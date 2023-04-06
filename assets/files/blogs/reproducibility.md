
# Reproducibility

-   Complete Reproducibility is not confirmed in Pytorch but there are so randomness that we can control
-   We can also configure pytorch to avoid using non deterministic algorithms for some operations, so multiple call gives us the same results
    -    meaning we are using deterministic algorithms that gives the same results even for multiple calls


-   Mannual Seed for Pytorch and Python

    ```
    import torch
    import random

    torch.manual_seed(0)
    random.seed(0)
    ```
-   The cuDNN library, used by CUDA convolution operations, can be a source of nondeterminism across multiple executions of an application. 
-   Avoiding nondeterministic algorithms
    -   `torch.use_deterministic_algorithms()` lets you configure PyTorch to use deterministic algorithms instead of nondeterministic ones where available, and to throw an error if an operation is known to be nondeterministic (and without a deterministic alternative
    ```
    torch.use_deterministic_algorithms(True)
    ```
    -   