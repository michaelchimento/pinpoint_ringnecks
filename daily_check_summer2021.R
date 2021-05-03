library(tidyverse)
library(lubridate)
setwd("/home/shared_projects/pinpoint_ringnecks")


file_names <- dir("coallated_data") #where you have your files
df_all <- do.call(rbind,lapply(paste("coallated_data/",file_names, sep=""),read.csv))
df_all = df_all %>% mutate(date = date(ymd_hms(time)))

df= df_all %>% filter(date>(ymd(Sys.Date())-5))

df_sum = df %>% mutate(id = as.factor(id)) %>% 
  group_by(camera_name,population,date,id) %>% summarize(sum = n())
mean(df_sum$sum)
p1 = ggplot(data=df_sum, aes(x=date,y=id))+
  facet_grid(population~camera_name,scales="free")+
  geom_tile(aes(fill=log(sum,10)))+
  scale_fill_distiller(palette = "Spectral", name="log10(detects)")+
  #geom_text(aes(label=sum),color="black",size=4)+
  scale_x_date(date_labels = "%b %d")+
  labs(y="ID",x="Day",title="Pinpoint detections: last 5 days")+
  theme_dark()
ggsave(p1,file="pinpoint_detections_heatmap.pdf",width=15,height=8, units="in")

