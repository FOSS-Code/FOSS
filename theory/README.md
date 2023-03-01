# Theoretical Analysis for FOSS
In this part, we conduct a theoretical analysis to prove that FOSS achieves a more effective feature selection than the completely random methods, and it is more adaptive for unknown class perception compared to the deterministic model. Moreover, we analyze its algorithmic complexity.

## Feature Perception of Node Split in FOSS

We will analyze the feature perception of the Monte Carlo method in FOSS in terms of feature selection effectiveness and loss of insensitive dimensions. Without special instructions, we use the following symbols: *FOSSForest* contains $t$ *FOSSTrees*, and all *FOSSTrees* reach the maximum tree height $h_{max}$, i.e., each leaf node experiences $h_{max}-1$ hyperplane partition. The analysis of *FOSSForest* in other states can also be generalized from this setting. 

(i) Effectiveness analysis of the feature selection. Considering $d$-dimension feature set, its weighted entropy $\mathbb{H} = \{H_q(1), \cdots, H_q(d)\}$ can be calculated by the following Equation. 

$$H_q = \sum\nolimits_{i = 1}^k {\frac{-p_i\log_2{p_i}}{|x_i - \mathbb{E}(S(q))|}}$$

If the weighted entropy value is large, it means that this dimension has great randomness, which could be inefficient for hyperplane partition. Assume that the dimensions which $H_q$ less threshold $T_h$ are regarded as the efficient features. And there are $N_f$ efficient dimensions for each feature selection, i.e., $len(\mathbb{H} < T_h) = N_f$, $N_f < d$. 
The probability that all paths of leaf nodes perform effective partitioning are $P_{{E}}= (  {N_f /d})^{{h_{max }} - 1}$ and 

$$P_{{E}}^{\prime} = {\left( {1 - \frac{{C_{d - N_f}^{{n_{\mathrm{sam}}}}}}{{C_d^{{n_{\mathrm{sam}}}}}}} \right)^{{h_{max }} - 1}} = {\left( {1 - \frac{{A_{d - N_f}^{{n_{\mathrm{sam}}}}}}{{A_d^{{n_{\mathrm{sam}}}}}}} \right)^{{h_{max }} - 1}}$$

for completely random methods and FOSS, respectively, where $n_{sam}$ refers to the number of candidate dimensions in the Monte Carlo method. We can obtain $P_{{E}}^{\prime} > {P_{{E}}}$ based on the following formula, which proves that FOSS can increase the selection probability of effective dimensions. 

$$1 - \frac{{A_{d - N_f}^{{n_{\mathrm{sam}}}}}}{{A_d^{{n_{\mathrm{sam}}}}}} - \frac{N_f}{d} = \frac{{\left( {d - N_f} \right)\left( {A_{d - 1}^{{n_{\mathrm{sam}}} - 1} - A_{d - 1 - N_f}^{{n_{\mathrm{sam}}} - 1}} \right)}}{{A_d^{{n_{\mathrm{sam}}}}}} > 0$$

This design alleviates the struggle under the high-dimensional feature space of completely random model construction. Thus, FOSS can improve the effectiveness of each hyperplane partition in the setting with a lack of ground-truth labels. 

(ii) Loss measure of the insensitive feature dimensions. So-called insensitive features refer to those dimensions that produce little effect for hyperplane partition based on the current data. To adapt to detect the unknown classes that could present completely different distributions from existing samples, these insensitive dimensions cannot be discarded directly. So we quantify the loss of the insensitive feature dimensions for the deterministic model and FOSS. Assume that there are $N_s$ ($N_s < d$) insensitive dimensions for each feature selection. Then the ignore probability of the insensitive dimensions by the deterministic model and FOSS are $P_{{I}}=1$ and 

$$P_{{I}}^{\prime} = {\left( {1 - \frac{{C_{d - N_s}^{{n_{\mathrm{sam}}}}}}{{C_d^{{n_{\mathrm{sam}}}}}}} \right)^{{h_{max }} - 1}} = {\left( {1 - \frac{{A_{d - N_s}^{{n_{\mathrm{sam}}}}}}{{A_d^{{n_{\mathrm{sam}}}}}}} \right)^{{h_{max }} - 1}} \ll P_{{I}}$$

Therefore, compared with the deterministic model that calculates the entropy of all dimensions for each selection, FOSS reserves the consideration of insensitive features with probability ${{C_{N_s}^{{n_{\mathrm{sam}}}}} / {C_d^{{n_{\mathrm{sam}}}}}}$. It facilitates feature-aware generalization to isolate the emerging attacks when running model inference. Overall, FOSS reconciles the completely random and deterministic by introducing the Monte Carlo method, which advances the trade-off between the existing-sample perception and future-instance generalization. 

## Time and Space Complexity

**Steps** | **Time Complexity** | **Space Complexity** 
:-: | :-: | :-: 
Extract feature | $O(dM)$ | $O(d|X_n|)$
Construct *FOSSForest* | $O(N_{tree}\psi n_{\mathrm{sam}} \log \psi)$ | $O(N_{tree}d\psi)$ 
Classify/detect outliers | $O(N_{tree}d\psi)$ | $O(N_{tree}d\psi)$ 
Assign fine-grained labels | $O(s \log s)$ | $O(ds)$ 
Update *FOSSForest* | $O(N_{tree}sn_{\mathrm{sam}} \log s)$ | $O(N_{tree}d(\psi + s))$ 
Total | $O\left( dM+N_{tree}n_{\mathrm{sam}} \\ (\psi \log \psi+s\log s) \\ +N_{tree}d\psi \right)$ | $O\left( d\|X_n\| + d \\ N_{tree}(\psi + s) \right)$ 

FOSS mainly consists of five parts: feature extraction, model construction, detection and classification, assign fine-grained labels, model update. We summarize the corresponding time and space complexity in the above Table. For the feature extraction, it needs $O(dM)$ time and $O(d|X_n|)$ space to generate $d$ features for $|X_n|$ flows by traversing $M$ packets. In the model-building stage, FOSS takes $O(N_{tree} \psi n_{\mathrm{sam}} \log \psi)$ time and $O(N_{tree}d\psi)$ space to create $N_{tree}$ *FOSSTrees*, which could be optimized by parallelization. To perform classification and outlier detection, constructing the isolation path anomaly and data cloud has a time complexity of $O(N_{tree}d\psi)$, and evaluating a sample requires $O(N_{tree}(\log \psi + d))$. Also the space complexity of the procedure is $O(N_{tree}d\psi)$. To assign the fine-grained label for outlier samples, it will impose $O(s \log s)$ time and $O(ds)$ space by isolation-based clustering, where $s$ denotes the buffer size. For the model update, the required time complexity and space complexity are similar to the model construction, just with different data sizes, are $O(N_{tree}sn_{\mathrm{sam}} \log s)$ and $O(N_{tree}d(\psi + s))$. 

In summary, the total time complexity is 
$O\left(	dM+N_{tree}n_{\mathrm{sam}}(\psi \log \psi +s\log s)+N_{tree}d\psi\right)$
and the space complexity is 
$O\left(d|X_n| + N_{tree}d(\psi + s)\right)$

Overall, the computational complexity of FOSS is proportional to the number of flows and packets. And FOSS does not have an operation with high time or space complexity that is higher than quadratic terms. Therefore, the whole process of FOSS introduces affordable low overhead. 
