import forum_analyzer.preprocessor.preprocessor as preproc
import src.database as db

link = input()
# db.add_group_to_postgres(link)
print(preproc.preprocessed_group(link))
