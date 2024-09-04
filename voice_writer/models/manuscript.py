from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from common.models import BaseModel
from .author import Author
from .voice import VoiceRecording


class ManuscriptType(models.TextChoices):
    ARTICLE = "article", "Article"
    BLOG_POST = "blog post", "Blog Post"
    BOOK = "book", "Book"
    ESSAY = "essay", "Essay"
    GUIDE = "guide", "Guide"
    LETTER = "letter", "Letter"
    MANUAL = "manual", "Manual"
    OTHER = "other", "Other"
    PLAY = "play", "Play"
    POEM = "poem", "Poem"
    REPORT = "report", "Report"
    RESEARCH_PAPER = "research paper", "Research Paper"
    REVIEW = "review", "Review"
    SCRIPT = "script", "Script"
    SHORT_STORY = "short story", "Short Story"
    THESIS = "thesis", "Thesis"


class SectionType(models.TextChoices):
    ABOUT_THE_AUTHOR = "about the author", "About the Author"
    ABSTRACT = "abstract", "Abstract"
    ACKNOWLEDGEMENTS = "acknowledgements", "Acknowledgements"
    ACKNOWLEDGMENTS = "acknowledgments", "Acknowledgments"
    ACT = "act", "Act"
    AFTERWORD = "afterword", "Afterword"
    ANNEXES = "annexes", "Annexes"
    APPENDIX = "appendix", "Appendix"
    BIBLIOGRAPHY = "bibliography", "Bibliography"
    CAST_LIST = "cast list", "Cast List"
    CHAPTER = "chapter", "Chapter"
    CHARACTER_LIST = "character list", "Character List"
    CONCLUSION = "conclusion", "Conclusion"
    COPYRIGHT_PAGE = "copyright page", "Copyright Page"
    COVER = "cover", "Cover"
    DEDICATION = "dedication", "Dedication"
    DISCUSSION = "discussion", "Discussion"
    EPILOGUE = "epilogue", "Epilogue"
    EXECUTIVE_SUMMARY = "executive summary", "Executive Summary"
    FOREWORD = "foreword", "Foreword"
    GLOSSARY = "glossary", "Glossary"
    INDEX = "index", "Index"
    INTRODUCTION = "introduction", "Introduction"
    LITERATURE_REVIEW = "literature review", "Literature Review"
    METHODOLOGY = "methodology", "Methodology"
    OTHER = "other", "Other"
    PREFACE = "preface", "Preface"
    PREFATORY_NOTE = "prefatory note", "Prefatory Note"
    PROLOGUE = "prologue", "Prologue"
    REFERENCES = "references", "References"
    RESULTS = "results", "Results"
    SCENE = "scene", "Scene"
    STAGE_DIRECTIONS = "stage directions", "Stage Directions"
    TABLE_OF_CONTENTS = "table of contents", "Table of Contents"
    TITLE_PAGE = "title page", "Title Page"


class Genres(models.TextChoices):
    ADVENTURE = "adventure", "Adventure"
    ART = "art", "Art"
    BIOGRAPHY = "biography", "Biography"
    CHILDREN = "children", "Children"
    COOKING = "cooking", "Cooking"
    DRAMA = "drama", "Drama"
    EDUCATION = "education", "Education"
    FANTASY = "fantasy", "Fantasy"
    FICTION = "fiction", "Fiction"
    HISTORY = "history", "History"
    HORROR = "horror", "Horror"
    HUMOR = "humor", "Humor"
    MULTI_GENRE = "multi_genre", "Multi-genre"
    MUSIC = "music", "Music"
    MYSTERY = "mystery", "Mystery"
    NON_FICTION = "non_fiction", "Non-Fiction"
    OTHER = "other", "Other"
    PHILOSOPHY = "philosophy", "Philosophy"
    POETRY = "poetry", "Poetry"
    RELIGION = "religion", "Religion"
    ROMANCE = "romance", "Romance"
    SCIENCE = "science", "Science"
    SCIENCE_FICTION = "science_fiction", "Science Fiction"
    SELF_HELP = "self_help", "Self-Help"
    THRILLER = "thriller", "Thriller"
    TRAVEL = "travel", "Travel"


class Manuscript(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=50,
        choices=ManuscriptType.choices,
        default=ManuscriptType.BOOK,
    )
    genre = models.CharField(
        max_length=50,
        choices=Genres.choices,
        default=Genres.FICTION,
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Section(BaseModel):
    type = models.CharField(
        max_length=50,
        choices=SectionType.choices,
        default=SectionType.CHAPTER,
    )
    manuscript = models.ForeignKey(
        Manuscript,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title} (Section {self.order})'


class Document(BaseModel):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    recordings = models.ManyToManyField(
        VoiceRecording,
        related_name='documents'
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    content = models.TextField(null=True, blank=True)
    content_json = models.JSONField(null=True, blank=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title} (Document {self.order})'


@receiver(pre_save, sender=Manuscript)
def pre_save_manuscript(sender, instance, **kwargs):
    # Set slug if not set
    if instance.id and instance.title and not instance.slug:
        first_octet = str(instance.id).split('-')[0]
        instance.slug = f"{slugify(instance.title).replace('-', '_')}_{first_octet}"