from mmengine import Config

from mmagic.registry import MODELS
from mmagic.utils import register_all_modules

import os
import torch
from pathlib import Path
import datetime
from mmagic.models.editors.animatediff import save_videos_grid



register_all_modules()

cfg = Config.fromfile('configs/animatediff/animatediff_ToonYou.py')
animatediff = MODELS.build(cfg.model).cuda()
prompts = ["(masterpiece, best quality), wasteland, wrecked train, moss, scenery, landscape, nature"
]

negative_prompts = [
    "worst quality, low quality, letterboxed",
    "badhandv4,easynegative,ng_deepnegative_v1_75t,verybadimagenegative_v1.3, bad-artist, bad_prompt_version2-neg, teeth",
    "",
    "",
]

sample_idx = 0
random_seeds = cfg.randomness['seed']
random_seeds = [random_seeds] if isinstance(random_seeds, int) else list(random_seeds)
samples = []
time_str = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
savedir = f"samples/{Path(cfg.model['dream_booth_lora_cfg']['type']).stem}-{time_str}"
os.makedirs(savedir)
for prompt_idx, (prompt, n_prompt, random_seed) in enumerate(zip(prompts, negative_prompts, random_seeds)):
    output_dict = animatediff.infer(prompt,negative_prompt=n_prompt, video_length=16, height=256, width=256, seed=random_seed,num_inference_steps=cfg.model['dream_booth_lora_cfg']['steps'])
    sample = output_dict['samples']
    prompt = "-".join((prompt.replace("/", "").split(" ")[:10]))
    save_videos_grid(sample, f"{savedir}/sample/{sample_idx}-{prompt}.gif")
    print(f"save to {savedir}/sample/{prompt}.gif")
    samples.append(sample)
    sample_idx += 1

samples = torch.concat(samples)
save_videos_grid(samples, f"{savedir}/sample.gif", n_rows=4)