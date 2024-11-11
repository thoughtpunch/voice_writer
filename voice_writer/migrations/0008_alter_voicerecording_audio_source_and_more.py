# Generated by Django 5.0.7 on 2024-11-10 14:05

import voice_writer.models.voice
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voice_writer', '0007_remove_voicerecording_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voicerecording',
            name='audio_source',
            field=models.CharField(blank=True, choices=[('app', 'App'), ('upload', 'Upload'), ('api', 'API')], default='app', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='voicerecording',
            name='cover',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=voice_writer.models.voice.recording_audio_upload_path),
        ),
        migrations.AlterField(
            model_name='voicerecording',
            name='duration_ms',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='voicerecording',
            name='language',
            field=models.CharField(blank=True, choices=[('ab', 'Abkhazian'), ('aa', 'Afar'), ('af', 'Afrikaans'), ('ak', 'Akan'), ('sq', 'Albanian'), ('am', 'Amharic'), ('ar', 'Arabic'), ('hy', 'Armenian'), ('as', 'Assamese'), ('av', 'Avaric'), ('ay', 'Aymara'), ('az', 'Azerbaijani'), ('ba', 'Bashkir'), ('eu', 'Basque'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('bi', 'Bislama'), ('bs', 'Bosnian'), ('br', 'Breton'), ('bg', 'Bulgarian'), ('my', 'Burmese'), ('ca', 'Catalan'), ('ch', 'Chamorro'), ('ce', 'Chechen'), ('ny', 'Chichewa'), ('zh', 'Chinese'), ('cv', 'Chuvash'), ('kw', 'Cornish'), ('co', 'Corsican'), ('cr', 'Cree'), ('hr', 'Croatian'), ('cs', 'Czech'), ('da', 'Danish'), ('dv', 'Divehi'), ('nl', 'Dutch'), ('dz', 'Dzongkha'), ('en', 'English'), ('eo', 'Esperanto'), ('et', 'Estonian'), ('ee', 'Ewe'), ('fo', 'Faroese'), ('fj', 'Fijian'), ('fi', 'Finnish'), ('fr', 'French'), ('ff', 'Fula'), ('gl', 'Galician'), ('lg', 'Ganda'), ('ka', 'Georgian'), ('de', 'German'), ('el', 'Greek'), ('gn', 'Guarani'), ('gu', 'Gujarati'), ('ht', 'Haitian'), ('ha', 'Hausa'), ('he', 'Hebrew'), ('hz', 'Herero'), ('hi', 'Hindi'), ('ho', 'Hiri Motu'), ('hu', 'Hungarian'), ('is', 'Icelandic'), ('io', 'Ido'), ('ig', 'Igbo'), ('id', 'Indonesian'), ('ia', 'Interlingua'), ('ie', 'Interlingue'), ('iu', 'Inuktitut'), ('ik', 'Inupiaq'), ('ga', 'Irish'), ('it', 'Italian'), ('ja', 'Japanese'), ('jv', 'Javanese'), ('kn', 'Kannada'), ('kr', 'Kanuri'), ('ks', 'Kashmiri'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('ki', 'Kikuyu'), ('rw', 'Kinyarwanda'), ('kv', 'Komi'), ('kg', 'Kongo'), ('ko', 'Korean'), ('ku', 'Kurdish'), ('kj', 'Kwanyama'), ('ky', 'Kyrgyz'), ('lo', 'Lao'), ('la', 'Latin'), ('lv', 'Latvian'), ('li', 'Limburgish'), ('ln', 'Lingala'), ('lt', 'Lithuanian'), ('lu', 'Luba-Katanga'), ('lb', 'Luxembourgish'), ('mk', 'Macedonian'), ('mg', 'Malagasy'), ('ms', 'Malay'), ('ml', 'Malayalam'), ('mt', 'Maltese'), ('gv', 'Manx'), ('mi', 'Maori'), ('mr', 'Marathi'), ('mh', 'Marshallese'), ('mn', 'Mongolian'), ('na', 'Nauru'), ('nv', 'Navajo'), ('ng', 'Ndonga'), ('ne', 'Nepali'), ('nd', 'North Ndebele'), ('se', 'Northern Sami'), ('no', 'Norwegian'), ('nb', 'Norwegian Bokmål'), ('nn', 'Norwegian Nynorsk'), ('oc', 'Occitan'), ('oj', 'Ojibwe'), ('or', 'Oriya'), ('om', 'Oromo'), ('os', 'Ossetian'), ('ps', 'Pashto'), ('fa', 'Persian'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pa', 'Punjabi'), ('qu', 'Quechua'), ('ro', 'Romanian'), ('rm', 'Romansh'), ('ru', 'Russian'), ('sm', 'Samoan'), ('sg', 'Sango'), ('sa', 'Sanskrit'), ('sc', 'Sardinian'), ('sr', 'Serbian'), ('sn', 'Shona'), ('ii', 'Sichuan Yi'), ('sd', 'Sindhi'), ('si', 'Sinhala'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('so', 'Somali'), ('nr', 'South Ndebele'), ('st', 'Southern Sotho'), ('es', 'Spanish'), ('su', 'Sundanese'), ('sw', 'Swahili'), ('ss', 'Swati'), ('sv', 'Swedish'), ('tl', 'Tagalog'), ('ty', 'Tahitian'), ('tg', 'Tajik'), ('ta', 'Tamil'), ('tt', 'Tatar'), ('te', 'Telugu'), ('th', 'Thai'), ('bo', 'Tibetan'), ('ti', 'Tigrinya'), ('to', 'Tonga'), ('ts', 'Tsonga'), ('tn', 'Tswana'), ('tr', 'Turkish'), ('tk', 'Turkmen'), ('tw', 'Twi'), ('ug', 'Uighur'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('ve', 'Venda'), ('vi', 'Vietnamese'), ('vo', 'Volapük'), ('wa', 'Walloon'), ('cy', 'Welsh'), ('fy', 'Western Frisian'), ('wo', 'Wolof'), ('xh', 'Xhosa'), ('yi', 'Yiddish'), ('yo', 'Yoruba'), ('za', 'Zhuang'), ('zu', 'Zulu')], default='en', max_length=2, null=True),
        ),
    ]
