# WordleParaulogic

You can use it to help you beat the games in [**THIS**](https://paraules-catalanes.herokuapp.com/) link.

As the hyped thing for the last week, and which we will not probably hear anything again, wordle is one of the new sensations. And inspired by it, and with the curiosity to try to solve it with programming. A similar situation happens to the Paraulógic game, although I have the sensation that this has been more popular on where I live than globally, contrary to Wordle's success.

Additionally, and inspired by the 3blue1brown video on the topic ([video](https://www.youtube.com/watch?v=v68zYyaEmEA&t=1459s)), the strategy to solve the Wordle game implies using the information theory and entropy to suggest the best word possible for the next entry, the one that is more probable while maximizing the information you extract from it.

As so I developed a solver for both Wordle and Paraulógic games in the Catalan language, which consists of a server and client-side programming web server with NodeJS and HTML.

## The data

I expected that there will be somewhere easily accessible some kind of Catalan dictionary to extract the dataset of words from, but to my surprise, this was probably one of the most difficult parts of the development, although at the end I found some datasets that, after cleaning them a little, were usable by the project. Still, I think that they are lacking in some words, for example, I haven't found filla (daughter) in the dataset.

The datasets come from basically one source (the Zipf one), although the other two have been used very lightly for finetuning.

-[**Zipf's laws of meaning in Catalan Datasets**](https://zenodo.org/record/4120887#.YhafMuj0m3D)
-[**Wikicorpus, v. 1.0: Catalan, Spanish and English portions of the Wikipedia**](https://www.cs.upc.edu/~nlp/wikicorpus/)
-[**Corpus textual informatitzat de la llengua catalana**](https://ctilc.iec.cat/)

## Usage

If you want to modify it on your own you are free to do it, I only ask for a mention if it's the case.

Remember to create your env file with the key to your MongoDB database in the CONNECTION_URL variable.

And modify the code necessary to make it work.

Good Luck!

## Extras

In this project there are also some python scripts code that I used to prepare the Database, that can be helpful to you if you are interested.

A demonstration also can be seen [**HERE**](https://drive.google.com/file/d/17FgpybzJLCQ9idTYtavIgG2Gu9SDLkDi/view?usp=sharing)

