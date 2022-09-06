###########################
### SIMILARITY ANALYSIS ###
###########################

library(mgcv)
library(mgcViz)

df = read.csv('/Users/edoardofilippi-mazzola/Desktop/NLP/Network analysis/class jaccard similarity/cit_sample_with_jaccard.csv')
df_2 = df[df[,'lag_days']>=0,]
df_2$sim = df_2$sim*100

#########################
### BINARY PREDICTORS ###
#########################

same_company = ifelse(df_2[,'owner_sender']==df_2[,'owner_receiver'],1,0)
same_company[df_2[,'owner_sender']==""] = 0
same_company[df_2[,'owner_receiver']==""] = 0

is_sender_big = ifelse(df_2[,'owner_sender']!="",1,0)
is_receiver_big = ifelse(df_2[,'owner_receiver']!="",1,0)

is_citation_big = ifelse((df_2[,'owner_sender']!= "") & (df_2[,'owner_receiver']!= ""),1,0)

df_2[,'same_company']    = same_company
df_2[,'is_sender_big']   = is_sender_big
df_2[,'is_receiver_big'] = is_receiver_big
df_2[,'is_citation_big'] = is_citation_big

df_2[,'log_sender_citations'] = log(df_2$sender_citation_count)

###############
### MODEL 0 ###
###############

mod0 = gam(sim~s(pub_date),data=df_2)
mod0 = getViz(mod0)
summary(mod0)
plot(mod0)

###############
### MODEL 1 ###
###############

mod1 = gam(sim~s(pub_date)+
             s(lag_days),
           data=df_2)

mod1 = getViz(mod1)
summary(mod1)
plot(mod1)

###############
### MODEL 2 ###
###############

mod2 = gam(sim~s(pub_date)+
             s(lag_days)+
             s(log_sender_citations)+
             same_company+
             is_sender_big+
             is_receiver_big,
           data=df_2)

mod2 = getViz(mod2)
summary(mod2)
plot(mod2)

###############
### MODEL 3 ###
###############

mod3 = gam(sim~s(pub_date)+
             s(lag_days)+
             s(log_sender_citations)+
             same_company+
             is_sender_big+
             is_receiver_big+
             jac_section+
             jac_class+
             jac_sub.class+
             jac_group+
             jac_sub.group,
           data=df_2)

mod3 = getViz(mod3)
summary(mod3)
plot(mod3)



