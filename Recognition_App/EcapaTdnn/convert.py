import torch
import torch.nn as nn
from torch.utils.mobile_optimizer import optimize_for_mobile

# 加载训练好的模型
from mvector.models.ecapa_tdnn import EcapaTdnn

backbone = EcapaTdnn(input_size=80, embd_dim=192)
model = nn.Sequential(backbone)
model.to(torch.device("cpu"))
# 加载模型
# model.load_state_dict(torch.load("models/CAMPPlus_Fbank/best_model/model.pth", map_location='cpu'), strict=False)
model.load_state_dict(torch.load("models/save/VoiceprintRecognition_Pytroch-超大数据集-MelSpectrogram/models/ecapa_tdnn_MelSpectrogram/best_model/model.pt", map_location='cpu'), strict=False)
# 设置为推理模式
model.eval()

# example = torch.rand(1, 13, 80)
# traced_script_module = torch.jit.trace(model, example)
# optimized_traced_model = optimize_for_mobile(traced_script_module)
# optimized_traced_model._save_for_lite_interpreter("android/model_lite.pt")

# 将训练好的模型转换为jit脚本模型
scripted_module = torch.jit.script(model)
# 优化jit脚本模型，提高在移动设备上的推理性能
optimized_scripted_module = optimize_for_mobile(scripted_module)

# 导出完整的jit版本模型(不兼容轻量化解释器)
scripted_module.save("android/3/model_script.pt")
# 导出轻量化解释器版本模型(与轻量化解释器兼容)
scripted_module._save_for_lite_interpreter("android/3/model_script_lite.pt")
# 使用优化的轻量化解释器模型比未优化的轻量化解释器模型推理速度快60%左右，比未优化的jit脚本模型推理速度快6%左右
optimized_scripted_module._save_for_lite_interpreter("android/3/model_script_optimized.pt")
