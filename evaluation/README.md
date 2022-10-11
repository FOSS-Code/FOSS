# Additional Evaluation for FOSS
## The defination of ACC and AMI

For $n$ samples in a dataset, let $y_i$ be the class label for the $i$-th sample and $\hat{y}_i$ the predicted value. $ACC$ is used to find the best match between the class labels $y$ and the predicted labels $\hat{y}$, so it is defined by:

$$
ACC(y, \hat{y}) = \max_{perm \in P} \frac{1}{n} \sum_{i=0}^{n-1} 1(perm(\hat{y}_i) = y_i)
$$

where $P$ is the set of all permutations in $[1,\cdots,K]$ and $K$ is the number of classes. $AMI$ removes feature bias by normalizing the Mutual Information ($MI$) between $y$ and $\hat{y}$ for the expected gain in entropy, as described below

$$
MI(y,\hat{y}) = \sum_{i=0}^{n-1} {\sum_{j=0}^{n-1} {p(y_i,\hat{y}_j)} } \log \left( {\frac{{p(y_i,\hat{y}_j)}}{{p(y_i)p(\hat{y}_j)}}} \right)
$$

$$
AMI(y,\hat{y}) = \frac{{MI(y,\hat{y}) - E[MI(y,\hat{y})]}}{{max(H(y),H(\hat{y})) - E[MI(y,\hat{y})]}}
$$

The function $p(y_i, \hat{y}_j)$ defines the joint probability of $y_i$ and $\hat{y}_j$, whereas $p(y_i)$ and $p(\hat{y}_j)$ are the individual probabilities of $y_i$ and $\hat{y}_j$ occurring respectively. Moreover, $E[\cdot]$ and $H(\cdot)$ represent the expected value and entropy, respectively. 

## Similarities between Different Attacks

<div align=center>
    <img src="similarities\cho2.png" width=300 height=300 />
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d7;
    display: inline-block;
    color: #999;
    padding: 2px;">Figure. The similarity evaluation between different attacks.</div>
</div>

Considering that the different divisions for known/unknown attack categories could lead to different detection effects, we further explore here the relationship between any two attacks. We solely use one attack as the known category to train FOSS and detect each attack from the remaining classes, respectively. The above figure depicts the relationship between the attacks. When solely using the XSS attack for training, 35.4% of Web brute force attack (Web BF, for short) instances will be identified as XSS attack, while 40.8% of XSS attack instances could be recognized as Web BF when trained only with Web BF. It can be attributed that both attacks are HTTP-based attacks and may be similar in terms of traffic features. Apart from that, other attacks have little similarity that is no misclassification into known attack classes. 
This implies that different dataset divisions will not have a great impact on FOSS. 

## Specific-Attack Feature Perception

As mentioned in appendix D of the paper, the visualization of the top ten dimensions of the SSH Patator samples is shown in the below figure. 

<div align=center>
    <img src="case\ssh.png" height=500 />
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d7;
    display: inline-block;
    color: #999;
    padding: 2px;">Figure. The per-dimensional scatterplot for SSH.</div>
</div>

### Case 2: SQL Injection

<div align=center>
    <img src="case\tsne2.png" height=300 />
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d7;
    display: inline-block;
    color: #999;
    padding: 2px;">Figure. Feature analysis and visualization for SQL Injection.</div>
</div>

We discuss here the feature perception for the SQL Injection case. In the above figure, it exhibits the top-10 and bottom-10 feature dimensions for the SQL Injection attack. Among them, the top-10 features including $(ttl: dim_{20}, dim_{22}, dim_{23})$; $(fin: dim_{43}, dim_{78})$; $(push: dim_{40}, dim_{75})$, $(value: dim_{33}, dim_{103})$. This indicates the representation of SQL Injection may have diversity. For example, a larger TTL helps the injection attack traffic reach the target machine as much as possible, manifested as $ttlmax$ in $dim$ = 20. On the contrary, the bottom-10 mainly contain dimensions that are not very relevant to this attack: such as $dim_{0}$: $pro$, $dim_{39}$: $urgfor$, $dim_{80}$: $flagmfbac$. The above figure (b) and (c) display the 2D distribution after dimensionality reduction with t-SNE based on the top-10 features and bottom-10 features respectively. Similar to Figure 13 in the paper, it is clear that subfigure (b) which uses the last 10 dimensions cannot portray SQL Injection well due to all sample distributions being messy. While in subfigure (c), the SQL Injection presents better separability compared to the instances of other types. We also plot the sample scatterplot for each dimension of the top-10 feature in the below figure. It shows that SQL Injection can be distinguished from the vast majority of other-categories samples on these key features. 

<div align=center>
    <img src="case\sql.png" height=500 />
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d7;
    display: inline-block;
    color: #999;
    padding: 2px;">Figure. The per-dimensional scatterplot for SQL.</div>
</div>

## Additional Details for Feature Masking

### Feature Masking Robustness.

<div align=center>
    <img src="adversarial\mask.png" height=350 />
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d7;
    display: inline-block;
    color: #999;
    padding: 2px;">Figure. The AMI curve (%) with feature masking.</div>
</div>

Given the aforementioned that FOSS possesses desirable feature perception, we intend to disable several-dimensional features to evaluate the robustness. To mask features, we use a sliding window to zero $W_d$-dimension feature at a time and then inspect the detection effect of FOSS, where $W_d = [1, 4, 16, 64]$ respectively. The experimental results are summarized in the above figure, where the $x$-axis refers to 106 dimensions and the $y$-axis represents the changed value of $AMI$ when masking the corresponding $x$ feature. The above figure (a)-(d) correspond $W_d = [1, 4, 16, 64]$ for the model with $N_k:N_u$ = $8:0$, subfigure (e)-(h) for $N_k:N_u$ = $0:8$, and the results of $N_k:N_u$ = $4:4$ in the below figure. For $W_d = [4, 16, 64]$, the features in the front and middle positions will be masked multiple times by the sliding window. So the solid line corresponds to the mean of multiple experiments, and the shaded areas reflect the maximum and minimum values. In vertical comparison, the $AMI$ will drop as the sliding window size of masking increases, e.g., the $AMI$ reduction value from ~0.2% to ~0.5% in $W_d = 1$ and $W_d = 64$. For horizontal comparison, the $AMI$ loss is more significant when there are more unknown classes, and it is up to about 7% $AMI$ loss when the sliding window size is 64 for the model with $N_k:N_u$ = $0:8$. 
In addition, we can find the peak positions of subfigures (a) and (e) are not exactly the same for the two model settings when $W_d = 1$. It implies that FOSS will tend to use different features when the training set changes, thereby the dimensions of the greatest influence by feature masking are also various. Interestingly, $AMI$ occasionally rose in all experimental groups which means that some features may be not very useful. In this situation, the preprocessing for dimensionality reduction or directly increasing the searches $n_{sam}$ of the Monte Carlo method could be beneficial. We perform some validation experiments in Section D.2 of the paper by varying the hyperparameters. 

<div align=center>
    <img src="adversarial\maskapp.png" height=200 />
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d7;
    display: inline-block;
    color: #999;
    padding: 2px;">Figure. The feature masking results of $N_k:N_u$ = $4:4$.</div>
</div>

The above figure (a)-(d) correspond $W_d = [1, 4, 16, 64]$ for the model with $N_k:N_u$ = $4:4$. For $W_d = [4, 16, 64]$, the features in the front and middle positions will be masked multiple times by the sliding window. So the solid line corresponds to the mean of multiple experiments, and the shaded areas reflect the maximum and minimum values. 
By comparing above two figures, it can be found that the AMI loss of the $N_k:N_u$ = $4:4$ ratio is between all known and all unknown.

## Real-World DDoS Attack Source

As mentioned in Section 6 of the paper, the partial IP addresses (after anonymous processing) of the attack source are visualized in the below figure. 

<div align=center>
    <img src="realworld\tuopu.png" height=500 />
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d7;
    display: inline-block;
    color: #999;
    padding: 2px;">Figure. The partial attack source diagram. We anonymize the IP address.</div>
</div>

## The details of the feature extraction

<div align=center style="color:orange; 
    color: #999;
    padding: 2px;">Table. The corresponding fields of feature extraction.
</div>

Dimensions | 0    | 1   | 2   | 3   | 4   | 5    | 6   | 7  | 8   | 9  
:-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-:   
Names | pro           | packnum      | timesum      | ack          | urg          | push          | reset        | syn         | fin          | flagdf    
Dimensions | 10   | 11  | 12  | 13  | 14  | 15   | 16  | 17 | 18  | 19   
Names | flagmf        | offset       | lenmax       | lenmin       | lenmean      | lenstd        | deltamax     | deltamin    | deltamean    | deltastd  
Dimensions | 20   | 21  | 22  | 23  | 24  | 25   | 26  | 27 | 28  | 29   
Names | ttlmax        | ttlmin       | ttlmean      | ttlstd       | sizemax      | sizemin       | sizemean     | sizestd     | factormax    | factormin     
Dimensions | 30   | 31  | 32  | 33  | 34  | 35   | 36  | 37 | 38  | 39   
Names | factormean    | factorstd    | valuemax     | valuemin     | valuemean    | valuestd      | packnumfor   | timesumfor  | ackfor       | urgfor        
Dimensions | 40   | 41  | 42  | 43  | 44  | 45   | 46  | 47 | 48  | 49   
Names | pushfor       | resetfor     | synfor       | finfor       | flagdffor    | flagmffor     | offsetfor    | lenmaxfor   | lenminfor    | lenmeanfor    
Dimensions | 50   | 51  | 52  | 53  | 54  | 55   | 56  | 57 | 58  | 59   
Names | lenstdfor     | deltamaxfor  | deltaminfor  | deltameanfor | deltastdfor  | ttlmaxfor     | ttlminfor    | ttlmeanfor  | ttlstdfor    | sizemaxfor    
Dimensions | 60   | 61  | 62  | 63  | 64  | 65   | 66  | 67 | 68  | 69   
Names | sizeminfor    | sizemeanfor  | sizestdfor   | factormaxfor | factorminfor | factormeanfor | factorstdfor | valuemaxfor | valueminfor  | valuemeanfor  
Dimensions | 70   | 71  | 72  | 73  | 74  | 75   | 76  | 77 | 78  | 79   
Names | valuestdfor   | packnumbac   | timesumbac   | ackbac       | urgbac       | pushbac       | resetbac     | synbac      | finbac       | flagdfbac     
Dimensions | 80   | 81  | 82  | 83  | 84  | 85   | 86  | 87 | 88  | 89   
Names | flagmfbac     | offsetbac    | lenmaxbac    | lenminbac    | lenmeanbac   | lenstdbac     | deltamaxbac  | deltaminbac | deltameanbac | deltastdbac   
Dimensions | 90   | 91  | 92  | 93  | 94  | 95   | 96  | 97 | 98  | 99   
Names | ttlmaxbac     | ttlminbac    | ttlmeanbac   | ttlstdbac    | sizemaxbac   | sizeminbac    | sizemeanbac  | sizestdbac  | factormaxbac | factorminbac  
Dimensions | 100  | 101 | 102 | 103 | 104 | 105  | | | |  
Names | factormeanbac | factorstdbac | valuemaxbac  | valueminbac  | valuemeanbac | valuestdbac | | | |
