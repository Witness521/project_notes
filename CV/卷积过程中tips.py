'''
标注两个初学者的点
    1. 卷积核(kernel_size)通常情况都是奇数，因为方便same padding时的处理，可以将padding补充的0放在两侧对称分布
    2. 在same padding时 padding的大小设置成kernel_size的一半


self.conv1 = nn.Conv2d(num_channels, 64, kernel_size=9, padding=9 // 2)
self.conv2 = nn.Conv2d(64, 32, kernel_size=5, padding=5 // 2)
self.conv3 = nn.Conv2d(32, num_channels, kernel_size=5, padding=5 // 2)
self.relu = nn.ReLU(inplace=True)
'''

'''
    当运行这样需要参数的代码
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-file', type=str, required=True)
    parser.add_argument('--eval-file', type=str, required=True)
    parser.add_argument('--outputs-dir', type=str, required=True)
    
    python train.py --train-file BLAH_BLAH/91-image_x3.h5 --eval-file BLAH_BLAH/Set5_x3.h5 --outputs-dir BLAH_BLAH/outputs
    直接--加参数名 参数值 即可 不需要加""
    
    参数名中的-在后面参数中会自动转成_
    e.g.  --outputs-dir -->  args.outputs_dir
'''

'''
    卷积核（kernel）和过滤器（filter）的区别
    1. 卷积核就是由长和宽来指定的，是一个二维的概念。
    2. 而过滤器是是由长、宽和深度指定的，是一个三维的概念。过滤器可以看做是卷积核的集合。
    
    即： 一个过滤器就对应一个特征图。
'''

'''
    机器学习中的ground truth
    在监督学习中，数据都是有标注的，以(x, t)的形式出现，其中x是输入数据，t是标注。 正确的t标注就是ground truth
'''