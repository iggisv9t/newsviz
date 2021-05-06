import argparse
import configparser
import os

config = configparser.ConfigParser()
parser = argparse.ArgumentParser()
parser.add_argument("--basedir", required=True)
parser.add_argument("--projname", required=True)

args = parser.parse_args()
print(args)
basedir = args.basedir
projname = args.projname

# Raw
rawdir = os.path.join(basedir, "data/raw")
os.makedirs(rawdir, exist_ok=True)
config["common"] = {"raw_path": rawdir}
# Classifier
prepdir = os.path.join(basedir, "data/processed")
os.makedirs(prepdir, exist_ok=True)
modelsdir_c = os.path.join(basedir, "models/classifier")
os.makedirs(modelsdir_c, exist_ok=True)
config["preprocessor"] = {
    "output_path": prepdir,
    "classifier_path": os.path.join(modelsdir_c, projname + ".bin"),
    "ftransformer_path": os.path.join(modelsdir_c, projname + "_trans.bin"),
}
# Topic
topicdir = os.path.join(basedir, "data/topic_model_ed")
os.makedirs(topicdir, exist_ok=True)
modelsdir_t = os.path.join(basedir, "models/topic_model")
os.makedirs(modelsdir_t, exist_ok=True)
config["topic"] = {
    "output_path": topicdir,
    "model_path": os.path.join(modelsdir_t, "tm_" + projname + "_{}.bin"),
    "dict_path": os.path.join(modelsdir_t, "dictionary_tm_" + projname + "_{}.bin"),
}
# Vis
vispath = os.path.join(basedir, "data/ready2viz")
os.makedirs(vispath, exist_ok=True)
config["visualizer"] = {"data_path": vispath}

confpath = f"../config/config_{projname}.ini"
with open(confpath, "w") as fp:
    config.write(fp)

print("Ready")
print(f"Place your data in {rawdir} directory for each source")
print(f"See or edit expected model names in {confpath}")
print("If models are ready, you can run full pipeline with command")
print(f"PYTHONPATH='.' luigi --module pipeline TopicPredictorTask --conf={confpath} --local-scheduler ")