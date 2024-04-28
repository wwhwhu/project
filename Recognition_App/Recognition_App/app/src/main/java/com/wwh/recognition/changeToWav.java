package com.wwh.recognition;

import android.media.MediaCodec;
import android.media.MediaExtractor;
import android.media.MediaFormat;
import android.media.MediaMuxer;
import android.os.Environment;

import java.io.IOException;
import java.nio.ByteBuffer;

public class changeToWav{

    public static void convert3gpToWav(String inputFilePath, String outputFilePath) throws IOException {
        MediaExtractor extractor = new MediaExtractor();
        extractor.setDataSource(inputFilePath);

        int trackIndex = -1;
        for (int i = 0; i < extractor.getTrackCount(); i++) {
            MediaFormat format = extractor.getTrackFormat(i);
            String mime = format.getString(MediaFormat.KEY_MIME);
            if (mime.startsWith("audio/")) {
                extractor.selectTrack(i);
                trackIndex = i;
                break;
            }
        }

        if (trackIndex < 0) {
            throw new RuntimeException("No audio track found in the input file");
        }

        MediaCodec.BufferInfo info = new MediaCodec.BufferInfo();
        MediaMuxer muxer = new MediaMuxer(outputFilePath, MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);

        int audioTrackIndex = muxer.addTrack(extractor.getTrackFormat(trackIndex));
        muxer.start();

        ByteBuffer buffer = ByteBuffer.allocate(1024 * 1024); // Adjust buffer size as needed
        int sampleSize;
        while ((sampleSize = extractor.readSampleData(buffer, 0)) >= 0) {
            info.size = sampleSize;
            info.presentationTimeUs = extractor.getSampleTime();
            muxer.writeSampleData(audioTrackIndex, buffer, info);
            extractor.advance();
        }

        muxer.stop();
        muxer.release();
        extractor.release();
    }
}

