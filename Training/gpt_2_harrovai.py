import gpt_2_simple as gpt2
import os
import requests

model_name = "355M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)

file_name = "all.txt"
sess = gpt2.start_tf_sess()

gpt2.finetune(sess,
              dataset=file_name,
              model_name=model_name,
              steps=1000,
              print_every=10,
              sample_every=200,
              save_every=500)

sess = gpt2.load_gpt2(gpt2.start_tf_sess(), run_name='run1', checkpoint_dir='checkpoint')

gpt2.generate(sess, prefix="", temperature=0.7, nsamples=5, batch_size=5)
