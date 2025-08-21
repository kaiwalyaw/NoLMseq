# Load required package
library(readxl)

# Change this to specific Excel file name:
file_name <- "bootstrap_pop1pop2.xlsx"   # <-- your file name
sheet_name <- 1  # Change if needed

# Read data
data <- read_excel(file_name, sheet = sheet_name)

group1 <- data[[1]]
group2 <- data[[2]]

# Actual t-test
actual_test <- t.test(group1, group2)
actual_p <- actual_test$p.value
cat("Observed p-value:", actual_p, "\n")

# Pool values for bootstrapping
pooled <- c(group1, group2)
n1 <- length(group1)
n2 <- length(group2)

# Set bootstrap iterations
n_iter <- 1000

# Perform bootstrap
sig_count <- 0
set.seed(42)  
# for reproducibility
for (i in 1:n_iter) {
  sampled <- sample(pooled)
  g1 <- sampled[1:n1]
  g2 <- sampled[(n1+1):(n1+n2)]
  t_res <- t.test(g1, g2)
  if (t_res$p.value <= actual_p) {
    sig_count <- sig_count + 1
  }
}

empirical_p <- sig_count / n_iter
cat("Number of random runs with p-value as small or smaller than observed:", sig_count, "out of", n_iter, "\n")
cat("Empirical p-value:", empirical_p, "\n")

# Save results
writeLines(c(
  paste0("Observed p-value: ", actual_p),
  paste0("Number of random runs ≤ observed p: ", sig_count, " out of ", n_iter),
  paste0("Empirical p-value: ", empirical_p)
), con = "bootstrap_results.txt")

cat("Results saved in bootstrap_results.txt\n")
