library(tidyverse)
library(lubridate)
setwd("/home/michael/pinpoint_ringnecks")


file_names <- dir("coallated_data") #where you have your files
fnames_social = file_names[grepl("Social",file_names)]
df_social <- do.call(rbind,lapply(paste("coallated_data/",fnames_social, sep=""),read.csv))
df_social = df_social %>% mutate(date = date(ymd_hms(time)),camera_type="social")

fnames_feeder = file_names[grepl("Feeder",file_names)]
df_feeder <- do.call(rbind,lapply(paste("coallated_data/",fnames_feeder, sep=""),read.csv))
df_feeder = df_feeder %>% mutate(date = date(ymd_hms(time)),camera_type="feeder")

df= rbind(df_feeder,df_social)

df_sum = df %>% mutate(id = as.factor(id),population=factor(population, c("P1","P2","P3","P4"))) %>% 
                        group_by(camera_type,population,date,id) %>% summarize(sum = n())
mean(df_sum$sum)
p1 = ggplot(data=df_sum %>% filter(camera_type=="social"), aes(x=date,y=id))+
  facet_wrap(~population,scales="free")+
  geom_tile(aes(fill=log(sum,10)))+
  scale_fill_distiller(palette = "Spectral", name="log10(detects)")+
  #geom_text(aes(label=sum),color="black",size=4)+
  scale_x_date(date_labels = "%b %d")+
  labs(y="ID",x="Day",title="Pinpoint detections: Social cams")+
  theme_dark()
ggsave(p1,file="pinpoint_detections_heatmap_social.pdf",width=15,height=8, units="in")

p1 = ggplot(data=df_sum %>% filter(camera_type=="feeder"), aes(x=date,y=id))+
  facet_wrap(~population,scales="free")+
  geom_tile(aes(fill=log(sum,10)))+
  scale_fill_distiller(palette = "Spectral", name="log10(detects)")+
  #geom_text(aes(label=sum),color="black",size=4)+
  scale_x_date(date_labels = "%b %d")+
  labs(y="ID",x="Day",title="Pinpoint detections: Feeder cams")+
  theme_dark()
ggsave(p1,file="pinpoint_detections_heatmap_feeder.pdf",width=15,height=8, units="in")

p1 = ggplot(data=df_sum, aes(x=date,y=id))+
  facet_wrap(~population,scales="free")+
  geom_tile(aes(fill=log(sum,10)))+
  scale_fill_distiller(palette = "Spectral", name="log10(detects)")+
  #geom_text(aes(label=sum),color="black",size=4)+
  scale_x_date(date_labels = "%b %d")+
  labs(y="ID",x="Day",title="Pinpoint detections: Combined")+
  theme_dark()
ggsave(p1,file="pinpoint_detections_heatmap_combined.pdf",width=15,height=8, units="in")
