- # This project is a toy project for training and quality assurance purposes

SET A:

The objective of this project is to get better answers for user queries from gpt-3 on a specific matter.
So, there can be some sectors, the data for those are not updated on gpt-3. To handle that,
we tried to follow the following steps:

- First we'll read the data we want to use in a specific case.
- We will divide in to some chunks.
- Transform the chunks in to vector using embedding algorithm
- Save the vectors to a vector database.
- If an user query appears, we'll find some best matches.
  So, these are the steps we do s preparation of dataset.
  Then,
  If a query appeared, we do the following:
- We first take the query and find matches with the data we have on vector database, like a semantic serch.
- We take those contexts, and generate a prompt appropriate to the use case, including the contexts and the user's original question. We tell gpt-3 to
  answer based on the context.

Note: The embedding model used here has 384 dimensions.

Useful Docs:

- [Openai](https://platform.openai.com/docs)
- [Pinecone](https://docs.pinecone.io/docs/quickstart)
- [HuggingFace](https://huggingface.co/models)

Tasks:

1. Load the text from the given docx file and split them in to some chunks. (A splitter is defined, you can use that.)
2. Add all the splitted chunks to the vector database. (Use addData function)
3. Create a prompt using the process discussed above.
4. Get the answer from gpt-3 api.
5. Get all the things together such that, we can pass a query using the function user_query and get a solid answer.
6. The embedding model we used here is a basic embedding model, change the model and use openai's embedding model 'text-embedding-ada-002'
7. Can we improve something in this process? Any suggestion you think of list it down.
8. Do you think you have a better idea to handle the whole process? Write a summary about the alternative approach.

SET B:
Problem:
Given these rules:

```
We have 5 ingredient:
oranges
apples
pears
grapes
watermelon
lemon
lime


Questions we ask client:
1.Do you go out to party on weekends? (yes or no)
2.What flavours do you like? (cider, sweet, waterlike)
3.What texture you don't like? (smooth, slimy, rough)
4.What price range will you buy drink for? ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)

If they party on weekends, apples, pears, grapes, watermelon are allowed.
If they like cider, show apples, oranges, lemon, lime.
If they like sweet, show watermelon, orange.
If they like waterlike, show watermelon.
If grapes is chosen, remove watermelon from the list.
If texture you don't like is smooth, remove pears.
If texture you don't like is slimy, remove watermelon, lime and grape.
If texture you don't like is waterlike, remove watermelon.
If price < $3 remove lime, watermelon.
If price > $4 and < $7 remove pears, apples.
```

Tasks:

1. Make a function passing in the answer to the 4 questions and structure GPT3 prompt given these rules to give you the list of recommeded fruits.
2. Make a simple flask POST API where we return the answers given the input in POST Body with content type application/json
