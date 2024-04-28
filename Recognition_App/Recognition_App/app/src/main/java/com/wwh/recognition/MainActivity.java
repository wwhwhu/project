package com.wwh.recognition;

import static com.wwh.recognition.changeType.computeMelSpectrogram;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.pytorch.IValue;
import org.pytorch.LiteModuleLoader;
import org.pytorch.Module;
import org.pytorch.Tensor;

import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.FloatBuffer;
import java.util.Arrays;

public class MainActivity extends AppCompatActivity {

    private Button button1;
    private Button button2;
    private Button button3;
    private MediaRecorder mediaRecorder;
    private boolean isRecording;
    private Module module;
    private final static int AUDIO_LEN_IN_SECOND = 3;
    private final static int SAMPLE_RATE = 32000;
    private final static int RECORDING_LENGTH = SAMPLE_RATE * AUDIO_LEN_IN_SECOND;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // 识别
        button1 = findViewById(R.id.button);
        // 新建录音保存
        button2 = findViewById(R.id.button2);
        // 删除已有录音
        button3 = findViewById(R.id.button3);
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO},
                    10);
        }
        button1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                newRecording();
            }
        });

        button2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                recoginize();
            }
        });

        button3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                deleteRecord();
            }
        });
    }

    private void deleteRecord(String fileName, boolean isToast) {
        File directory = getFilesDir(); // 获取应用的内部存储目录
        File fileToDelete = new File(directory, fileName);
        if (fileToDelete.exists()) {
            fileToDelete.delete();
            if (isToast) {
            Toast.makeText(MainActivity.this, "Record deleted", Toast.LENGTH_SHORT).show();
        }
    }}

    private void deleteRecord() {
        // 删除录音
        File directory = getFilesDir(); // 获取应用的内部存储目录
        File[] files = directory.listFiles();

        if (files != null && files.length > 0) {
            // 弹出列表供用户选择删除
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("Record List");

            // 将文件名转换为字符串数组
            final String[] fileNames0 = new String[files.length];
            int j = 0;

            for (int i = 0; i < files.length; i++) {
                String fileName = files[i].getName();
                if (fileName.endsWith(".wav")) {
                    fileNames0[j] = fileName.replace(".wav", "");
                    j++;
                }
            }

            final String[] fileNames = new String[j];
            for (int i = 0; i < j; i++) {
                fileNames[i] = fileNames0[i];
            }
            builder.setItems(fileNames, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    String selectedFileName = fileNames[which];
                    deleteRecord(selectedFileName + ".wav", true);
                }
            });

            // 添加取消按钮
            builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {
                            // 用户取消操作
                            dialog.dismiss();
                        }
                    }
            );
            builder.show();
        } else {
            Toast.makeText(MainActivity.this, "No records found", Toast.LENGTH_SHORT).show();
        }
    }

    private void newRecording() {
        // 新建录音
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("New Record Name");
        final EditText input = new EditText(this);
        builder.setView(input);
        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String newRecordName = input.getText().toString();
                if (newRecordName.isEmpty()) {
                    Toast.makeText(MainActivity.this, "Record name cannot be empty", Toast.LENGTH_SHORT).show();
                    return;
                }
                boolean isSameNameExists = checkSameNameExists(newRecordName);
                if (!isSameNameExists) {
                    isRecording = true;
                    changeButtonColor(button1, "录音中..."); // 改变按钮1的颜色表示录音中
                    button2.setEnabled(false); // 禁用按钮2
                    button3.setEnabled(false); // 禁用按钮3
                    startRecording(newRecordName, 1);
                } else {
                    Toast.makeText(MainActivity.this, "Same name record already exists", Toast.LENGTH_SHORT).show();
                }
            }
        });
        builder.setNegativeButton("Cancel", null);
        builder.show();
    }

    private void recoginize() {
        // 首先开始录音
        isRecording = true;
        changeButtonColor(button2, "录音中..."); // 改变按钮1的颜色表示录音中
        button1.setEnabled(false); // 禁用按钮1
        button3.setEnabled(false); // 禁用按钮3
        startRecording("temp", 2);
    }

    private boolean checkSameNameExists(String recordName) {
        // 检查应用的私有数据目录是否存在同名记录
        File directory = getFilesDir(); // 获取应用的内部存储目录
        Log.d("Check Record Files", directory.getAbsolutePath());
        File[] files = directory.listFiles();
        // 打印当前已有的文件名
        if (files != null) {
            if (files.length > 0) {
                for (File file : files) {
                    Log.d("Record Files", file.getName());
                    if (file.getName().equals(recordName + ".wav")) {
                        return true;
                    }
                }
            }
        } else
            Log.d("Record Files", "No files");
        return false;
    }

    private void changeButtonColor(Button button, String text) {
        if (isRecording) {
            // 设置为红色，不可点击
            button.setBackgroundColor(Color.argb(255, 171, 13, 102));
            button.setText(text);
            button.setEnabled(false);
        } else {
            // 设置为绿色，可点击
            button.setBackgroundColor(Color.argb(255, 23, 171, 13));
            if (text.equals("正在推理...")) {
                button.setBackgroundColor(Color.argb(255, 194, 255, 10));
                button.setText(text);
                button.setEnabled(false);
            } else {
                button.setBackgroundColor(Color.argb(255, 23, 171, 13));
                button.setText(text);
                button.setEnabled(true);
            }
        }
    }

    private void startRecording(String name, int index) {
        if (isRecording) {
            mediaRecorder = new MediaRecorder();
            mediaRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
            mediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
            mediaRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

            File directory = getFilesDir(); // 获取应用的内部存储目录
            File outputFile = new File(directory, name + ".3gp");
            mediaRecorder.setOutputFile(outputFile.getAbsolutePath());

            try {
                mediaRecorder.prepare();
                mediaRecorder.start();
                isRecording = true;

                // 三秒后停止录音
                new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        stopRecording(name, index);
                    }
                }, 3000);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void stopRecording(String name, int index) {
        if (isRecording) {
            mediaRecorder.stop();
            mediaRecorder.release();
            mediaRecorder = null;
            isRecording = false;
            Toast.makeText(MainActivity.this, "Recording stopped", Toast.LENGTH_SHORT).show();
            File directory = getFilesDir(); // 获取应用的内部存储目录
            String inputFilePath = directory.getAbsolutePath() + "/" + name + ".3gp";
            String outputFilePath = directory.getAbsolutePath() + "/" + name + ".wav";
            try {
                changeToWav.convert3gpToWav(inputFilePath, outputFilePath);
                // 删除3gp文件
                File fileToDelete = new File(inputFilePath);
                if (fileToDelete.exists()) {
                    fileToDelete.delete();
                }
            } catch (IOException e) {
                e.printStackTrace();
                // Conversion failed
                Log.d("Conversion", "Failed");
            }
            Log.d("model", "wav save success!");
            if (index == 1) {
                changeButtonColor(button1, "新建语音记录"); // 改变按钮1的颜色表示录音结束
                button2.setEnabled(true);
                button3.setEnabled(true);
            } else {
                changeButtonColor(button2, "正在推理..."); // 改变按钮2的颜色表示录音结束
                // 读取wav文件为float数组
                try {
                    String p = directory.getAbsolutePath() + "/temp.wav";
                    // 读取模型推理
                    float temp[] = inference(p);
                    deleteRecord("temp.wav",false);
                    // 计算每个其他wav的feature与temp.wav的feature的相似度
                    Log.d("Check Record Files", directory.getAbsolutePath());
                    File[] files = directory.listFiles();
                    // 相似度数组
                    float[] similarities = new float[files.length];
                    String[] names = new String[files.length];
                    int i = 0, j = 0;
                    // 打印当前已有的文件名
                    if (files != null && files.length > 0) {
                        for (File file : files) {
                            Log.d("Record Files", file.getName());
                            if (file.getName().endsWith(".wav") && !file.getName().equals("temp.wav")) {
                                String path = directory.getAbsolutePath() + "/" + file.getName();
                                float[] feature = inference(path);
                                double similarity = CosineSimilarity(temp, feature);
                                Log.d("Similarity", file.getName() + ": " + similarity);
                                similarities[i] = (float) Math.abs(similarity);
                                names[i] = file.getName();
                                j++;
                            } else {
                                similarities[i] = -1;
                                names[i] = file.getName();
                            }
                            i++;
                        }
                    } else {
                        Log.d("Record Files", "No files");
                    }
                    if (j == 0) {
                        Toast.makeText(MainActivity.this, "没有语音记录", Toast.LENGTH_SHORT).show();
                    }
                    // 找到最相似的语音记录
                    float max = similarities[0];
                    int maxIndex = 0;
                    for (int k = 1; k < similarities.length; k++) {
                        if (similarities[k] > max) {
                            max = similarities[k];
                            maxIndex = k;
                        }
                    }
                    Log.d("Max Similarity", names[maxIndex] + ": " + max);
                    if (max > 0.6) {
                        Log.d("model", "最大相似度为" + max + "，匹配成功，相似的名称为" + names[maxIndex].replace(".wav", ""));
                        Toast.makeText(MainActivity.this, "最大相似度为" + max + "，匹配成功，相似的名称为" + names[maxIndex].replace(".wav", ""), Toast.LENGTH_LONG).show();
                    } else {
                        Log.d("model", "最大相似度为" + max + "，匹配失败，可能没有录入数据库");
                        Toast.makeText(MainActivity.this, "最大相似度为" + max + "，匹配失败，可能没有录入数据库", Toast.LENGTH_LONG).show();
                    }
                } catch (IOException e) {
                    Log.e("model", "Failed");
                    e.printStackTrace();
                }
                changeButtonColor(button2, "开始语音识别");
                button1.setEnabled(true);
                button3.setEnabled(true);
            }
        }

    }

    private String assetFilePath(Context context, String assetName) {
        File file = new File(context.getFilesDir(), assetName);
        if (file.exists() && file.length() > 0) {
            return file.getAbsolutePath();
        }

        try (InputStream is = context.getAssets().open(assetName)) {
            try (OutputStream os = new FileOutputStream(file)) {
                byte[] buffer = new byte[4 * 1024];
                int read;
                while ((read = is.read(buffer)) != -1) {
                    os.write(buffer, 0, read);
                }
                os.flush();
            }
            return file.getAbsolutePath();
        } catch (IOException e) {
            Log.e("Model", assetName + ": " + e.getLocalizedMessage());
        }
        return null;
    }

    private float[] inference(String p) throws IOException {
        float[] audioData = readFromWav(p);
        // Log.d("model", "Wav Float Array: \n" + Arrays.toString(audioData));
        if (module == null) {
            module = LiteModuleLoader.load(assetFilePath(getApplicationContext(), "model_script_optimized.ptl"));
        }
        float[][] input = foredeal(audioData);
        // input转置
        float[][] inputT = new float[input[0].length][input.length];
        for (int i = 0; i < input.length; i++) {
            for (int j = 0; j < input[0].length; j++) {
                inputT[j][i] = input[i][j];
            }
        }
        Log.d("model", "inference input shape: " + inputT.length + " * " + inputT[0].length);
        // 将数据转换为模型可接受的Tensor
        FloatBuffer inTensorBuffer = Tensor.allocateFloatBuffer(input.length * input[0].length);
        for (float[] array : inputT) {
            inTensorBuffer.put(array); // 填充 FloatBuffer
        }
        inTensorBuffer.rewind(); // 重置 FloatBuffer 的位置到开始处，以便正确读取
        Tensor inTensor = Tensor.fromBlob(inTensorBuffer, new long[]{1, inputT.length, inputT[0].length});
        IValue iv = module.forward(IValue.from(inTensor));
        float result[] = iv.toTensor().getDataAsFloatArray();
        Log.d("model", "inference output: " + Arrays.toString(iv.toTensor().getDataAsFloatArray()));
        return result;
    }

    private float[][] foredeal(float[] floatInputBuffer) {
        // 先做归一化
        float mean = 0.0f;
        float std = 0.0f;
        // 计算均值
        for (int i = 0; i < floatInputBuffer.length; i++) {
            mean += floatInputBuffer[i];
        }
        mean /= floatInputBuffer.length;
        // 计算标准差
        for (int i = 0; i < floatInputBuffer.length; i++) {
            std += (floatInputBuffer[i] - mean) * (floatInputBuffer[i] - mean);
        }
        std = (float) Math.sqrt(std / floatInputBuffer.length);
        // 归一化
        for (int i = 0; i < floatInputBuffer.length; i++) {
            floatInputBuffer[i] = (floatInputBuffer[i] - mean) / std;
        }
        // 转化为MelSpectrogram
        return computeMelSpectrogram(floatInputBuffer);
    }

    private float[] readFromWav(String filePath) throws IOException {
        File file = new File(filePath);
        byte[] data = new byte[(int) file.length()];

        FileInputStream inputStream = new FileInputStream(file);
        inputStream.read(data);
        inputStream.close();

        int bytesPerSample = 2; // 对于 16 位 PCM，每个样本占据 2 个字节
        int numSamples = data.length / bytesPerSample;

        float[] audioData = new float[numSamples];
        // 将每个采样转换为浮点数
        ByteBuffer buffer = ByteBuffer.wrap(data);
        buffer.order(ByteOrder.LITTLE_ENDIAN); // WAV 文件通常使用 little-endian 格式
        for (int i = 0; i < numSamples; i++) {
            short sample = buffer.getShort();
            float sampleValue = sample / 32768f; // 将采样值归一化到 -1 到 1 之间
            audioData[i] = sampleValue;
        }
        return audioData;
    }

    private float[] fore(float[] array)
    {
        // 找到数组中的最大值和最小值
        float min = array[0];
        float max = array[0];
        for (int i = 1; i < array.length; i++) {
            if (array[i] < min) {
                min = array[i];
            }
            if (array[i] > max) {
                max = array[i];
            }
        }
        // 对数组进行归一化处理
        float[] normalizedArray = new float[array.length];
        for (int i = 0; i < array.length; i++) {
            normalizedArray[i] = (float) ((array[i] - min) / (max - min) * Math.PI);
        }
        return normalizedArray;
    }

    private double CosineSimilarity(float[] feature1, float[] feature2) {
        // 归一化feature1与feature2
        feature1 = fore(feature1);
        feature2 = fore(feature2);
        double dotProduct = 0.0;
        double normA = 0.0;
        double normB = 0.0;
        for (int i = 0; i < feature1.length; i++) {
            dotProduct += feature1[i] * feature2[i];
            normA += Math.pow(feature1[i], 2);
            normB += Math.pow(feature2[i], 2);
        }
        return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
    }
}


//

//

//}
