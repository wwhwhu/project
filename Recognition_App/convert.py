import torch
import torch.nn as nn
from torch.utils.mobile_optimizer import optimize_for_mobile

# script需要改变模型forward的书写方式，但是结构不变
# class Res2Conv1dReluBn(nn.Module):
#     def __init__(self, channels, kernel_size=1, stride=1, padding=0, dilation=1, bias=False, scale=4):
#         super().__init__()
#         assert channels % scale == 0, "{} % {} != 0".format(channels, scale)
#         self.scale = scale
#         self.width = channels // scale
#         self.nums = scale if scale == 1 else scale - 1
#
#         self.convs = []
#         self.bns = []
#         for i in range(self.nums):
#             self.convs.append(nn.Conv1d(self.width, self.width, kernel_size, stride, padding, dilation, bias=bias))
#             self.bns.append(nn.BatchNorm1d(self.width))
#         self.convs = nn.ModuleList(self.convs)
#         self.bns = nn.ModuleList(self.bns)
#
#     def forward(self, x):
#         out = []
#         spx = torch.split(x, self.width, 1)
#         # for i in range(self.nums):
#         #     if i == 0:
#         #         sp = spx[i]
#         #     else:
#         #         sp = sp + spx[i]
#         #     # Order: conv -> relu -> bn
#         #     sp = self.convs[i](sp)
#         #     sp = self.bns[i](F.relu(sp))
#         #     out.append(sp)
#         sp = spx[0]
#         for i, (conv, bn) in enumerate(zip(self.convs, self.bns)):
#             if i != 0:
#                 sp = sp + spx[i]
#             sp = conv(sp)
#             sp = bn(F.relu(sp))
#             out.append(sp)
#         if self.scale != 1:
#             out.append(spx[self.nums])
#         out = torch.cat(out, dim=1)
#         print(out.shape)
#         return out

# 加载训练好的模型
from mvector.models.ecapa_tdnn import EcapaTdnn

backbone = EcapaTdnn(input_size=80, embd_dim=192)
model = nn.Sequential(backbone)
model.to(torch.device("cpu"))
# 加载模型
model.load_state_dict(torch.load("models/CAMPPlus_Fbank/best_model/model.pth", map_location='cpu'), strict=False)
# 设置为推理模式
model.eval()

# example = torch.rand(1, 298, 80)
# traced_script_module = torch.jit.trace(model, example)
# optimized_traced_model = optimize_for_mobile(traced_script_module)
# optimized_traced_model._save_for_lite_interpreter("android/model_lite.pt")

# 将训练好的模型转换为jit脚本模型
scripted_module = torch.jit.script(model)
# 优化jit脚本模型，提高在移动设备上的推理性能
optimized_scripted_module = optimize_for_mobile(scripted_module)

# 导出完整的jit版本模型(不兼容轻量化解释器)
scripted_module.save("android/model_script.pt")
# 导出轻量化解释器版本模型(与轻量化解释器兼容)
scripted_module._save_for_lite_interpreter("android/model_script_lite.ptl")
# 使用优化的轻量化解释器模型比未优化的轻量化解释器模型推理速度快60%左右，比未优化的jit脚本模型推理速度快6%左右
optimized_scripted_module._save_for_lite_interpreter("android/model_script_optimized.ptl")
