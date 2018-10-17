library(ggplot2)
library(dplyr)
library(fpp)
library(forecast)

data = read.csv('C:/Users/Soomin/Google Drive/04. Study/0. NYC Data Science/1. Projects/2. Scraping/dt5.csv')
head(data)
data$price


tsdt = ts(data)

# Stationary tests: all stationary
Acf(data$Return_daily)
Pacf(data$Return_daily)

Acf(data$polarity)
Pacf(data$subjectivity)

Acf(data$numPosts_rate)
Pacf(data$numPosts_rate)

Box.test(data$Return_daily, lag=10, type="Ljung-Box")
Box.test(data$numPosts_rate, lag=10, type="Ljung-Box")
Box.test(data$polarity, lag=10, type="Ljung-Box")

adf.test(data$Return_daily, alternative = "stationary")
adf.test(data$numPosts_rate, alternative = "stationary")
adf.test(data$subjectivity, alternative = "stationary")

kpss.test(data$Return_daily)
kpss.test(data$numPosts_rate)
kpss.test(data$polarity)


# CCF
data$numPosts_rate[data$numPosts_rate=='Inf'] = 0
ccfvalues = ccf(data$polarity, data$Return_daily, 10)
ccfvalues



user_dt = read.csv('C:/Users/Soomin/Google Drive/04. Study/0. NYC Data Science/1. Projects/2. Scraping/user_dt.csv')
head(user_dt)

ggplot(user_dt, aes(x=user_followers, y=polarity)) +
  geom_point() #+
  #geom_smooth(method=lm)

user_lm = lm(polarity ~ . -user_ID -subjectivity, data = user_dt)
summary(user_lm)

user_lm = lm(subjectivity ~ . -user_ID -polarity, data = user_dt)
summary(user_lm)

user_lm = lm(user_posts  ~ . -user_ID, data = user_dt)
summary(user_lm)


# remove users having more than 30 times of moderating boards
part_dt_userremoved = read.csv('C:/Users/Soomin/Google Drive/04. Study/0. NYC Data Science/1. Projects/2. Scraping/dt4.csv')
head(part_dt_userremoved) 
ccfvalues = ccf(part_dt_userremoved$numPosts, data$Return_daily)
ccfvalues
lm = lm(Return_daily ~ . -Open -High -Low -Close -Adj.Close -Volume -Date -Date.1, data = part_dt_userremoved)
summary(lm)

library(Hmisc)

part_dt_userremoved = read.csv('C:/Users/Soomin/Google Drive/04. Study/0. NYC Data Science/1. Projects/2. Scraping/dt4.csv')
part_dt_userremoved$L1_numPosts = Lag(part_dt_userremoved$numPosts, 1)
part_dt_userremoved$L2_numPosts = Lag(part_dt_userremoved$numPosts, 2)
part_dt_userremoved$L3_numPosts = Lag(part_dt_userremoved$numPosts, 3)

part_dt_userremoved$L1_polarity = Lag(part_dt_userremoved$polarity, 1)
part_dt_userremoved$L2_polarity = Lag(part_dt_userremoved$polarity, 2)
part_dt_userremoved$L3_polarity = Lag(part_dt_userremoved$polarity, 3)

part_dt_userremoved$L1_subjectivity = Lag(part_dt_userremoved$subjectivity, 1)
part_dt_userremoved$L2_subjectivity = Lag(part_dt_userremoved$subjectivity, 2)
part_dt_userremoved$L3_subjectivity = Lag(part_dt_userremoved$subjectivity, 3)

lm = lm(Return_daily ~ L2_numPosts+L2_subjectivity+L2_polarity, 
        data = part_dt_userremoved)
summary(lm)

class(part_dt_userremoved)
part_dt_userremoved[3000:3050, c('Date','numPosts', 'L1_numPosts')]
head(part_dt_userremoved)
