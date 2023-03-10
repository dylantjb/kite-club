# Generated by Django 4.1.3 on 2023-03-10 20:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogs", "0003_books"),
    ]

    operations = [
        migrations.DeleteModel(
            name="books",
        ),
        migrations.AlterField(
            model_name="club",
            name="theme",
            field=models.CharField(
                choices=[
                    ("E", "Ebooks"),
                    ("A", "Arts"),
                    ("BM", "Biographies & Memoirs"),
                    ("BI", "Business & Investing"),
                    ("C", "Comics"),
                    ("CT", "Computers & Technology"),
                    ("CF", "Cookery, Food & Wine"),
                    ("F", "Fantasy"),
                    ("FL", "Fiction & Literature"),
                    ("G", "Gardening"),
                    ("HF", "Health & Fitness"),
                    ("HM", "Health, Mind & Body"),
                    ("H", "History"),
                    ("M", "Mystery & Thrillers"),
                    ("N", "Nature"),
                    ("P", "Poetry"),
                    ("PC", "Politics & Current Affairs"),
                    ("R", "Reference"),
                    ("RO", "Romance"),
                    ("RS", "Religion & Spirituality"),
                    ("S", "Science"),
                    ("SF", "Science Fiction"),
                    ("SP", "Sports"),
                    ("T", "Travel"),
                    ("Y", "Young Adult"),
                ],
                default="",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="favourite_genre",
            field=models.CharField(
                choices=[
                    ("NO", "None"),
                    ("E", "Ebooks"),
                    ("A", "Arts"),
                    ("BM", "Biographies & Memoirs"),
                    ("BI", "Business & Investing"),
                    ("C", "Comics"),
                    ("CT", "Computers & Technology"),
                    ("CF", "Cookery, Food & Wine"),
                    ("F", "Fantasy"),
                    ("FL", "Fiction & Literature"),
                    ("G", "Gardening"),
                    ("HF", "Health & Fitness"),
                    ("HM", "Health, Mind & Body"),
                    ("H", "History"),
                    ("M", "Mystery & Thrillers"),
                    ("N", "Nature"),
                    ("P", "Poetry"),
                    ("PC", "Politics & Current Affairs"),
                    ("R", "Reference"),
                    ("RO", "Romance"),
                    ("RS", "Religion & Spirituality"),
                    ("S", "Science"),
                    ("SF", "Science Fiction"),
                    ("SP", "Sports"),
                    ("T", "Travel"),
                    ("Y", "Young Adult"),
                ],
                default=("NO", "None"),
                max_length=2,
            ),
        ),
    ]