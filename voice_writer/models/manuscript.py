from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from common.models import BaseModel
from .author import Author
from .voice import VoiceRecording


class ManuscriptType(models.TextChoices):
    BOOK = "book", "Book"
    RESEARCH_PAPER = "research paper", "Research Paper"
    ARTICLE = "article", "Article"
    ESSAY = "essay", "Essay"
    BLOG_POST = "blog post", "Blog Post"
    THESIS = "thesis", "Thesis"
    SHORT_STORY = "short story", "Short Story"
    POEM = "poem", "Poem"
    SCRIPT = "script", "Script"
    PLAY = "play", "Play"
    REVIEW = "review", "Review"
    REPORT = "report", "Report"
    LETTER = "letter", "Letter"
    MANUAL = "manual", "Manual"
    GUIDE = "guide", "Guide"
    OTHER = "other", "Other"


class SectionType(models.TextChoices):
    # Common Book Parts
    COVER = "cover", "Cover"
    TITLE_PAGE = "title page", "Title Page"
    COPYRIGHT_PAGE = "copyright page", "Copyright Page"
    DEDICATION = "dedication", "Dedication"
    TABLE_OF_CONTENTS = "table of contents", "Table of Contents"
    FOREWORD = "foreword", "Foreword"
    PREFACE = "preface", "Preface"
    ACKNOWLEDGMENTS = "acknowledgments", "Acknowledgments"
    INTRODUCTION = "introduction", "Introduction"
    PROLOGUE = "prologue", "Prologue"
    CHAPTER = "chapter", "Chapter"
    EPILOGUE = "epilogue", "Epilogue"
    AFTERWORD = "afterword", "Afterword"
    APPENDIX = "appendix", "Appendix"
    GLOSSARY = "glossary", "Glossary"
    BIBLIOGRAPHY = "bibliography", "Bibliography"
    INDEX = "index", "Index"
    ABOUT_THE_AUTHOR = "about the author", "About the Author"
    # Additional Parts for Non-Fiction, Research Papers, and Theses
    ABSTRACT = "abstract", "Abstract"
    EXECUTIVE_SUMMARY = "executive summary", "Executive Summary"
    LITERATURE_REVIEW = "literature review", "Literature Review"
    METHODOLOGY = "methodology", "Methodology"
    RESULTS = "results", "Results"
    DISCUSSION = "discussion", "Discussion"
    CONCLUSION = "conclusion", "Conclusion"
    REFERENCES = "references", "References"
    ANNEXES = "annexes", "Annexes"
    ACKNOWLEDGEMENTS = "acknowledgements", "Acknowledgements"
    # Movie Script Parts
    CHARACTER_LIST = "character list", "Character List"
    ACT = "act", "Act"
    SCENE = "scene", "Scene"
    CAST_LIST = "cast list", "Cast List"
    STAGE_DIRECTIONS = "stage directions", "Stage Directions"
    OTHER = "other", "Other"


class Genres(models.TextChoices):
    FICTION = "fiction", "Fiction"
    NON_FICTION = "non_fiction", "Non-Fiction"
    MYSTERY = "mystery", "Mystery"
    SCIENCE_FICTION = "science_fiction", "Science Fiction"
    FANTASY = "fantasy", "Fantasy"
    BIOGRAPHY = "biography", "Biography"
    HISTORY = "history", "History"
    ROMANCE = "romance", "Romance"
    HORROR = "horror", "Horror"
    THRILLER = "thriller", "Thriller"
    SELF_HELP = "self_help", "Self-Help"
    PHILOSOPHY = "philosophy", "Philosophy"
    POETRY = "poetry", "Poetry"
    DRAMA = "drama", "Drama"
    ADVENTURE = "adventure", "Adventure"
    SCIENCE = "science", "Science"
    RELIGION = "religion", "Religion"
    TRAVEL = "travel", "Travel"
    HUMOR = "humor", "Humor"
    COOKING = "cooking", "Cooking"
    ART = "art", "Art"
    MUSIC = "music", "Music"
    EDUCATION = "education", "Education"
    CHILDREN = "children", "Children"
    MULTI_GENRE = "multi_genre", "Multi-genre"
    OTHER = "other", "Other"


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