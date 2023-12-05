using CSV
using DataFrames  
using CategoricalArrays
using MixedModels, StatsModels

# Import dataset from github.
df = CSV.read("/home/harrison/Desktop/gitHubRepos/Datasets/hierMarketing.csv", DataFrame)

# Rename dataframe columns. 
rename!(df, Dict(:const  => :cons))
rename!(df, Dict("resp.id" => :respID))

# Convert tp categorical
df.cons = categorical(df.cons);
df.speed = categorical(df.speed);
df.height = categorical(df.height);
df.respID = categorical(df.respID);

# Fit mixed model. 
fm = @formula(rating ~ speed + height + cons + theme + (speed + height + cons + theme | respID))
fit1 = fit(MixedModel, fm, df)
println(fit1)
#println(fixef(fit1))
#println(ranef(fit1))