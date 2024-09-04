# Generated by Django 5.0.7 on 2024-08-26 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voice_writer', '0002_alter_voicerecording_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manuscript',
            name='genre',
            field=models.CharField(choices=[('adventure', 'Adventure'), ('art', 'Art'), ('biography', 'Biography'), ('children', 'Children'), ('cooking', 'Cooking'), ('drama', 'Drama'), ('education', 'Education'), ('fantasy', 'Fantasy'), ('fiction', 'Fiction'), ('history', 'History'), ('horror', 'Horror'), ('humor', 'Humor'), ('multi_genre', 'Multi-genre'), ('music', 'Music'), ('mystery', 'Mystery'), ('non_fiction', 'Non-Fiction'), ('other', 'Other'), ('philosophy', 'Philosophy'), ('poetry', 'Poetry'), ('religion', 'Religion'), ('romance', 'Romance'), ('science', 'Science'), ('science_fiction', 'Science Fiction'), ('self_help', 'Self-Help'), ('thriller', 'Thriller'), ('travel', 'Travel')], default='fiction', max_length=50),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='type',
            field=models.CharField(choices=[('article', 'Article'), ('blog post', 'Blog Post'), ('book', 'Book'), ('essay', 'Essay'), ('guide', 'Guide'), ('letter', 'Letter'), ('manual', 'Manual'), ('other', 'Other'), ('play', 'Play'), ('poem', 'Poem'), ('report', 'Report'), ('research paper', 'Research Paper'), ('review', 'Review'), ('script', 'Script'), ('short story', 'Short Story'), ('thesis', 'Thesis')], default='book', max_length=50),
        ),
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.CharField(choices=[('about the author', 'About the Author'), ('abstract', 'Abstract'), ('acknowledgements', 'Acknowledgements'), ('acknowledgments', 'Acknowledgments'), ('act', 'Act'), ('afterword', 'Afterword'), ('annexes', 'Annexes'), ('appendix', 'Appendix'), ('bibliography', 'Bibliography'), ('cast list', 'Cast List'), ('chapter', 'Chapter'), ('character list', 'Character List'), ('conclusion', 'Conclusion'), ('copyright page', 'Copyright Page'), ('cover', 'Cover'), ('dedication', 'Dedication'), ('discussion', 'Discussion'), ('epilogue', 'Epilogue'), ('executive summary', 'Executive Summary'), ('foreword', 'Foreword'), ('glossary', 'Glossary'), ('index', 'Index'), ('introduction', 'Introduction'), ('literature review', 'Literature Review'), ('methodology', 'Methodology'), ('other', 'Other'), ('preface', 'Preface'), ('prefatory note', 'Prefatory Note'), ('prologue', 'Prologue'), ('references', 'References'), ('results', 'Results'), ('scene', 'Scene'), ('stage directions', 'Stage Directions'), ('table of contents', 'Table of Contents'), ('title page', 'Title Page')], default='chapter', max_length=50),
        ),
    ]
