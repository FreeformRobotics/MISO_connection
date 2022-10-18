# MISO_connection

**Welcome!**

This README file briefly introduces the meaning of each python file and some statistical results of experimental data.

**The content is described as follows:**

├── code  <br/>
│   ├── IM: Pointer_Pairing functions and their usage.  <br/>
│   ├── TBB: EXP_Pairing functions and their usage.  <br/>
│   ├── configuration_pointer: An example of how to maintain a library with configuration pointers  <br/>
│   ├── data_generation: The code used to generate the original data in the"/data/Matrix" folder  <br/>
│   ├── enumerate_configuration_space: Method of enumerating configuration space  <br/>
│   ├── example_human: The example in section VI.B of the article  <br/>
│   └── other_algorithms：Other methods proposed by other articles.   <br/>

├── data  <br/>
│   ├── Matrix1：Empty  <br/>
│   ├── Matrix2：Empty  <br/>
│   ├── Matrix3：Empty  <br/>
│   ├── Matrix4：Empty  <br/>
│   ├── Matrix22：Empty  <br/>
│   ├── Matrix23：Empty  <br/>
│   ├── Matrix24：Empty  <br/>
│   └── results：Intermediate results obtained when the author runs on the local computer  <br/>
└── results: Reproduced results by the Code Ocean platform  <br/>

The size of the original data in the folder "/data/Matrix" is up to 30GB, and we cannot upload it to the repository. The code to generate the original data is in ‘/code/data_generation’, and all the codes for generating the intermediate data are also included in the corresponding folder. It is recommended to download the code to a local computer for reproduction. 



**Correspondence between the names used in the code and the names used in the article**

IM/POINTER_Pairing.py: The IM algorithm

IM/CON_Pairing.py: The Modified Greedy-CM algorithm

IM/Greedy_CM.py: Author-written unmodified Greedy-CM algorithm

TBB/EXP_Pairing.py: The TBB algorithm

Matrix 1: For each $n=3, \cdots, 1000$, we generate two adjacency matrices with dimensions $n$ satisfying the conditions that each row has at most one $1$, and each column has at most eleven $1$'s. The experiment results are shown in Fig. 12

Matrix 2: Denote $b$ as the exact number of bifurcation modules in the configuration, $\hat{b}$ as the upper bound of the number of bifurcation modules in the configuration. The second group of matrices are 997 pairs of $X^I$ and $X^F$ with generation conditions, $n=1000$ and $\hat{b}=3, \cdots, 1000$. The experiment results are shown in Fig. 13(a)

Matrix 3: The third group of matrices are 496 pairs of $X^I$ and $X^F$ with generation conditions, $n=1000$ and $b=3, \cdots, 499$. The experiment results are shown in Fig. 13(b)

Matrix 4: Denote $\parallel b^I −b^F \parallel $ as the difference between $b$ of the initial configuration and $b$ of the final configuration. The fourth group of matrices are 496 pairs of $X^I$ and $X^F$ with generation conditions, $n=1000$ and $\parallel b^I −b^F \parallel =3, \cdots, 499$. The experiment results are shown in Fig. 13(c)

Matrix 22: $X^I$ and $X^F$ with generation conditions, $n=31$ and $\hat{b} =3, \cdots, 30$. The experiment results are shown in Fig. 13(e)

Matrix 23: $X^I$ and $X^F$ with generation conditions, $n=31$ and $b =3, \cdots, 13$. The experiment results are shown in Fig. 13(e)

Matrix 24: $X^I$ and $X^F$ with generation conditions, $n=31$ and $\parallel b^I −b^F \parallel =3, \cdots, 8$. The experiment results are shown in Fig. 13(e)

 **Comparison of various algorithms when inputting different matrices in Matrix1 folder**


The result of IM is better than local-procrustes and Modified Greedy-CM.

 ```
python /code/IM/draw_exp_mat1.py
python /code/IM/draw_exp_mat1_230.py
python /code/IM/draw_exp_mat1_35.py
 ```
 
 
**Comparison of various algorithms when inputting matrices in Matrix2 folder**


when $\hat{b}$ in the configuration is small, the number of reconfiguration steps calculated by the IM algorithm is much smaller than the average number.
 
```
python /code/IM/draw_graph_mat2.py
 ```
 
 **Comparison of various algorithms when inputting different matrices in Matrix3 folder**

The upward trend is because the increase of $b$ makes the configuration more complex. The downward trend is because when $b$ gradually approaches the limit $\frac{n-2}{2}$, the configuration contains more modules with an out-degree of 2. These modules and the leaf modules connected to them can be matched at the same time mostly. 

```
python /code/IM/draw_graph_mat3.py
 ```
 
**Comparison of various algorithms when inputting different matrices in Matrix4 folder**

```
python /code/IM/draw_graph_mat4.py
 ```
 
 **The reading ability of the configuration pointer**
 
 Encoding and reading ability when facing matrices of different dimensions $n$.
 ```
python /code/configuration_pointer/draw_encode_read_times_linear.py
 ```
Encoding and reading ability when facing matrices of the same dimension $n=200$.
```
python /code/configuration_pointer/draw_encode_read_times200.py
```
 
 **The example in section VI.B of the article**

In this example, the number of reconfiguration steps calculated by the IM algorithm is 91, and the number of reconfiguration steps calculated by the Modified Greedy-CM algorithm is 99. For example, four brown attachment positions outside the bifurcation modules are required by Modified Greedy-CM but reduced by the IM algorithm. 

 ```
#The initial configuration 
python /code/example_human/draw_final_human.py
#The final configuration
python /code/example_human/draw_initial_human.py
 ```

