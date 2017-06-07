library(syuzhet)

input_path <- "/Users/deborah/Documents/scripts/python_work/project2016/smelly_london/Full text"

files <- list.files(
  path=input_path,
  pattern="txt",
  recursive=FALSE
)
result <- lapply(files, function(file_name) {
  #print while processing
  cat("processing", file_name, "\n")
  moh <- get_text_as_string(paste(input_path, file_name, sep="/"))
  #tokenise by sentence
  moh_sentences <- get_sentences(moh)
  syuzhet_vector <- get_sentiment(moh_sentences, method="syuzhet")
  #write.table(syuzhet_vector, paste(output_path, file_name, sep="/"))
  #to convert a vector to a list of vectors of leangth 1 then to dataframe
  x <- c(file_name, sum(syuzhet_vector), summary(syuzhet_vector))
  names(x) <- c("fileName", "sum", "min", "1stQ", "median", "mean", "3rdQ", "max")
  data.frame(as.list(x))
})
 do.call("rbind", result)
 
write.table(result, file="/Users/deborah/Documents/sentiment-moh.csv", row.names=FALSE, col.names=FALSE, sep=",")

