# Radcliffe Clustering Experiment

##GetWordLists function used for processing the Radcliffe chunks 
getWordLists<-function(text.lines){
  text<-paste(text.lines, collapse=" ")
  words.lower<-tolower(text)
  words.list<-strsplit(words.lower, "\\W|_")
  word.vector<-unlist(words.list)
  book.freqs<-table(word.vector[which(word.vector!="")]) # Table puts it into types and tokens
  book.freqs.rel<-100*(book.freqs/sum(book.freqs))
  return(book.freqs.rel)
}

inputDir<-"radcliffe_p3"
files<-dir(path=inputDir, pattern=".*txt")

book.list.freqs<-list() # a list object to hold the results
for(i in 1:length(files)){
  text.lines<-scan(paste(inputDir, files[i], sep="/"), what="character", sep="\n")
  worddata<-getWordLists(text.lines)
  book.list.freqs[[files[i]]]<-worddata
}

freqs.list<-mapply(data.frame, ID=seq_along(book.list.freqs), book.list.freqs, SIMPLIFY=FALSE, MoreArgs=list(stringsAsFactors=FALSE))
freqs.df<-do.call(rbind, freqs.list)
result<-xtabs(Freq ~ ID+Var1, data=freqs.df)
final.m<-apply(result, 2, as.numeric)

smaller.m <- final.m[,apply(final.m,2,mean)>=.25]
dm<-dist(smaller.m) # Creates a distance object
cluster <- hclust(dm) # Performs a cluster analysis on the distance object
cluster$labels<-names(book.list.freqs) #get the book file names to use as lables.
plot(cluster) # plots the results as a dendrogram for our inspection.
# OR in one line
plot(hclust(dist( final.m[,apply(final.m,2,mean)>=2.5] )), labels<-names(book.list.freqs))
