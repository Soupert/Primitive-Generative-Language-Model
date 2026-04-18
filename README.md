# Primitive-Generative-Language-Model
A primitive, lightweight language model built off of Markov chains.
Use the Dataset Processor to compile the data into a file and the Quote Generator to generate a quote from it.
A default compiled dataset is included, but be aware that every time you run the Dataset Processor it will overwrite the previous one.
Discord integration sometime maybe.

---
# Instructions
Data can be imported by a link or a file name. If you wish to import a file, store it in the data folder. Do not include the path or file extension

After entering the data source to import, you will be prompted to input the following parameters
* **Max Chain Length** is the maximum number of previous words the model will be able to reference when picking the next word in a sentence, like a short-term memory. The larger your dataset, the longer you can make this without diminishing returns
* **Weight X** is the likelyhood that the model will choose to reference back by X words. It is reccomended to make your middle weights the biggest, and your first weights the smallest (EX: 7, 25, 15)
* **Line Delimited** is a toggle option which treats newlines as conclusive to a sentence when on. You will usually want to leave this on, but things like the Shakespeare dataset will work better with it off.

# Data
The datasets which come preloaded in the data folder is as such
* [2016 Trump campaign speeches](https://raw.githubusercontent.com/ryanmcdermott/trump-speeches/master/speeches.txt) - filename "trump"
* [Several Shakespeare plays](https://www.cs.princeton.edu/courses/archive/spring20/cos302/files/shakespeare.txt) - filename "shakespeare"
* [The Book of Psalms](https://www.cs.princeton.edu/~bwk/tpop.webpage/psalms.txt) - filename "psalms"

If you find any more interesting datasets that you think work well with this model, contact me and I'll add them to the preloaded sets
