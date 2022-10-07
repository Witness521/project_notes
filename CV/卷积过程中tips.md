### 一、标注两个初学者的点

    1. 卷积核(kernel_size)通常情况都是奇数，因为方便same padding时的处理，可以将padding补充的0放在两侧对称分布
    2. 在same padding时 padding的大小设置成kernel_size的一半
`
    self.conv1 = nn.Conv2d(num_channels, 64, kernel_size=9, padding=9 // 2)
    self.conv2 = nn.Conv2d(64, 32, kernel_size=5, padding=5 // 2)
    self.conv3 = nn.Conv2d(32, num_channels, kernel_size=5, padding=5 // 2)
    self.relu = nn.ReLU(inplace=True)
`

### 二、当运行这样需要参数的代码
`
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-file', type=str, required=True)
    parser.add_argument('--eval-file', type=str, required=True)
    parser.add_argument('--outputs-dir', type=str, required=True)
`
python train.py --train-file BLAH_BLAH/91-image_x3.h5 --eval-file BLAH_BLAH/Set5_x3.h5 --outputs-dir BLAH_BLAH/outputs
直接--加参数名 参数值 即可 不需要加""

参数名中的-在后面参数中会自动转成_
e.g.  --outputs-dir -->  args.outputs_dir


### 三、卷积核（kernel）和过滤器（filter）的区别
1. 卷积核就是由长和宽来指定的，是一个二维的概念。
2. 而过滤器是是由长、宽和深度指定的，是一个三维的概念。过滤器可以看做是卷积核的集合。

即： 一个过滤器就对应一个特征图。



### 四、机器学习中的ground truth
在监督学习中，数据都是有标注的，以(x, t)的形式出现，其中x是输入数据，t是标注。 正确的t标注就是ground truth

baseline:
所谓baseline，就是用最原始最简单的方法实现任务。(因此就有了strong baseline的概念，可以用较强的对比组模型)
将baseline作为对照，我们不断提升算法性能，不然没有对比，无法体现算法的优劣。

### 五、Ablation Study - 消融实验
将最终的模型进行简化，以研究模型中不同部分(components)的影响
立场提取和推理网络中的消融实验
1. 验证post-reply pair的作用，消融成只使用post和reply的平均向量去做classification
2. 消融掉推理图网络，只使用所有立场表示的平均值进行检测
3. 忽略模型中的可视化信息，并保持其他组件不变
4. 消融掉句子引导的注意力层，直接把文本特征和图片特征聚合为此模型中的多模态特征代表



### 六、上采样和反卷积
上采样一些常见的方法有：近邻插值（nearest interpolation）、双线性插值(bilinear interpolation)，双三次插值（Bicubic interpolation），
反卷积(Transposed Convolution)，反池化(Unpooling)

<div align=center><img src="pic/img1.png" style="zoom: 67%;"><br>
<img src="pic/img2.png" style="zoom: 67%;"></div>

[链接](https://www.zhihu.com/question/328891283/answer/1604072340)

### 七、 膨胀卷积（空洞卷积、扩张卷积）

**感受野(receptive field)**的Defination：：CNN中，某一层输出结果中一个元素所对应的输入层的区域大小，感受野是卷积核在图像上看到的大小，例如3×3卷积核的感受野大小为9。越大的感受野包含越多的上下文关系。

感受野的计算：[感受野计算的连接](https://blog.csdn.net/program_developer/article/details/80958716)

以**单层**的卷积来说，在普通的3×3卷积核完成卷积之后，原5×5特征图变成3×3，即：3×3特征图上的像素点的感受野为5×5（注明：在最后一层卷积操作的感受野就等于卷积核的大小）

对于**多层**卷积来说：

<img src="H:\files\python_file\project_notes\CV\pic\image-20220917202144425.png" alt="image-20220917202144425" style="zoom: 50%;" />

<img src="H:\files\python_file\project_notes\CV\pic\image-20220917202330421.png" alt="image-20220917202330421" style="zoom: 67%;" />

三层3×3卷积核操作之后的感受野是7*7，其中卷积核的步长为1，padding为0

感受野的计算方法采用从后向前计算：$RF_i=(RF_{i+1}-1)\times stride_i+Ksize_i$



- 膨胀卷积与普通的卷积相比：除了卷积核的大小以外，还有一个扩张率(dilation rate)参数，主要用来表示膨胀的大小。
- 膨胀卷积与普通卷积的相同点在于：卷积核的大小是一样的，在神经网络中即参数数量不变，区别在于膨胀卷积具有更大的感受野。
- 对比传统的conv操作，3层3x3的卷积加起来，stride为1的话，只能达到(kernel-1)*layer+1=7的感受野，也就是和层数layer成线性关系，而dilated conv的感受野是指数级的增长。

<div align=center><img src="H:\files\python_file\project_notes\CV\pic\image-20220917191103020.png" alt="image-20220917191103020" style="zoom: 67%;" /></div>



空洞卷积产生的问题：栅格效应

多个相同膨胀率的空洞卷积堆叠：

<img src="H:\files\python_file\project_notes\CV\pic\image-20220917220044853.png" alt="image-20220917220044853" style="zoom:67%;" />



解决方法：Hybrid Dilated Convolution（HDC) 混合膨胀卷积  [链接](https://www.cnblogs.com/yanshw/p/16128989.html)

1. 锯齿结构

​    dilated rate设计成了锯齿状结构，例如[1, 2, 5, 1, 2, 5]这样的循环结构 

锯齿状本身的性质就比较好的来同时满足小物体大物体的分割要求(小 dilation rate 来关心近距离信息，大 dilation rate 来关心远距离信息)。 这样卷积依然是连续的，依然能满足VGG组观察的结论，大卷积是由小卷积的 regularisation 的 叠加。

2. 公约数不能大于 1
