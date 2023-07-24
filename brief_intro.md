# Bionic Air Vehicle Cluster

This is a brief introduction of my bachelor's thesis.  
> *Research on Self-organization Behavior of the Bionic Flapping-wing Air Vehicle Cluster Based on Local Information Interaction*

## Research on the Mechanism and Formation of Bionic Flapping-wing Air Vehicle Cluster Formation Flight

In my research, the aerodynamic model of individual and cluster of bionic flapping-wing air vehicle is established, and by analyzing the distribution of vortices in the fluttering process, the energy efficient formation flight distance is calculated.

![仿生扑翼机个体照片](毕设资料/论文插图/图/%E6%89%91%E7%BF%BC%E6%9C%BA%E7%AE%80%E5%8C%96%E6%A8%A1%E5%9E%8B.png)
*<center>Simplied Model</center>*

![仿生扑翼机群体照片](毕设资料/论文插图/图/2-2.png "仿生扑翼机群体模型")
*<center>Schematic of Pelican Bird Spacing and Wingtip Vortices</center>*

## Two Technical Model of Self-organizing Behavior of Bionic Flapping-wing Air Vehicle CLuster  

We selects visual interaction as the form of local information interaction, proposes the self-organized behavior model of the bionic flapping-wing air vehicle cluster based on Couzin model and the self-organized behavior model of the bionic flapping-wing air vehicle cluster based on obstacle avoidance, and elaborates the above models from the aspects of mathematical model and algorithm design.  

### A Technical Model of Self-organizing Behavior of Bionic Flapping-wing Air Vehicle Cluster Based on Couzin Model  

![Couzin模型图](毕设资料/论文插图/流程图/Couzin模型图.png "Couzin模型图")  
*<center>Couzin Model</center>*

![个体邻域](毕设资料/论文插图/流程图/邻域集合.png "个体邻域")
*<center>Individual Neighborhood</center>*

![决策流程图](毕设资料/论文插图/流程图/基于Couzin模型的仿生扑翼机集群自组织行为算法示意图.png)
*<center>Algorithm for Self-organizing Behavior of Bionic Flapping-wing Air Vehicle Clusters Based on Couzin Model</center>*

After designing the algorithm for self-organizing bahavior of bionic flapping-wing air vehicle clusters base on Couzin model, we used *Python3* to test and verify the feasibility.

![Python实验图](毕设资料/论文插图/流程图/python仿真实验图.png)
*<center>Simulation of Bionic Flapping-wing Air Vehicle Self-organizing Behavier Algorithm Based on Couzin Model</center>*

### Optimazation Algorithm for Self-Organizing Behavioral Techniques of Bionic Flapping-wing Air Vehicle Based on Field of View Range  
  
![个体视野](毕设资料/论文插图/流程图/个体视野范围.png)
*<center>View Range of Individual</center>*  
  
![个体避障](毕设资料/论文插图/流程图/个体避障示意图.png)
*<center>Collision Avoidance of Indicidual</center>*
  
![算法决策](毕设资料/论文插图/流程图/基于避障性的仿生扑翼机集群自组织行为算法示意图.png)
*<center>Algorithm for Self-organizing Behavior of Bionic Flapping-wing Air Vehicle Clusters Based on Couzin Model and Collision Avoidance</center>*  
  
## Simulation  

Finally, a simulation environment is established in a platform named NetLogo, and the feasibility of the two proposed self-organization behavior models of the bionic flapping-wing air vehicle based on local information interaction with high-efficiency and energy-saving functions is verified.

![实验环境](毕设资料/论文插图/流程图/实验环境.png)
*<center>Simulation Environment</center>*

### Algorithm Based on Couzin Model

![Couzin初始图](毕设资料/论文插图/流程图/Couzin模型初始化.png)
*<center>Initialized Simulation Environment</center>*
  
![Couzin实验图](毕设资料/论文插图/流程图/Couzin实验图.png)
*<center>Simulation Process of First Algorithm</center>

![坠机数量](毕设资料/论文插图/图/1.png)
*<center>Number of Air Vehicle Crashes</center>*
  
### Algorithm Based on Couzin Model and Collision Advoidance

![避障性初始图](毕设资料/论文插图/流程图/避障性模型初始化.png)
*<center>Initialized Simulation Environment</center>*

![避障性实验图](毕设资料/论文插图/流程图/避障性实验图.png)
*<center>Simulation Process of Second Algorithm</center>*
  
![坠机数量](毕设资料/论文插图/图/2.png)
*<center>Number of Air Vehicle Crashes</center>*