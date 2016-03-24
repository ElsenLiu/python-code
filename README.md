# python-code

**CaffeLogParser** 

从Caffe Log文件中提取train loss, test loss, test accuracy并作图保存到文件中

使用方法：

python CaffeLogParser.py -i LOGPATH -o OUTFOLDER

python CaffeLogParser.py -h 查看帮助

生成Caffe Log，需要修改train.sh

```
#!/usr/bin/env sh 

LOG=train-`date +%Y-%m-%d-%H-%M-%S`.log
CAFFE=$CAFFE_ROOT/build/tools/caffe
SOLVER=$SOLVER_PATH

$CAFFE train --solver=$SOLVER --gpu=0 2>&1 | tee $LOG
```

**MTDImage** 根据urls多线程下载图片，未优化，有50%几率失败


