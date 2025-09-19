# api/management/commands/seed_posts.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
import random

from api.models import Category, Tag, Post

class Command(BaseCommand):
    help = "Seed the database with realistic categories, tags and N blog posts."

    def add_arguments(self, parser):
        parser.add_argument("--posts", type=int, default=100, help="Number of posts to create")
        parser.add_argument("--clear", action="store_true", help="Delete existing Category/Tag/Post objects first")

    def handle(self, *args, **options):
        # import Faker here to avoid failing import-time if package missing
        try:
            from faker import Faker
        except Exception:
            self.stderr.write(self.style.ERROR(
                "Faker not installed. Install it with `pip install Faker` and add to requirements.txt"
            ))
            return

        fake = Faker()

        posts_to_create = options["posts"]
        clear = options["clear"]

        if clear:
            self.stdout.write("Clearing existing Posts/Tags/Categories...")
            Post.objects.all().delete()
            Tag.objects.all().delete()
            Category.objects.all().delete()

        categories = [
            "Technology","Business","Lifestyle","Travel","Food","Health & Fitness",
            "Science","Education","Finance","Entertainment","Sports","Development"
        ]
        category_objs = []
        for name in categories:
            obj, _ = Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            category_objs.append(obj)

        tag_names = [
            "python","django","deployment","aws","react","javascript","productivity",
            "remote-work","startup","marketing","seo","recipes","nutrition","wellness",
            "mental-health","fitness","research","education","personal-finance","investing",
            "movies","music","football","nba","travel-tips","budget-travel","photography",
            "tutorial","testing","ci-cd","docker","kubernetes","data-science","ai","ml",
            "cloud","security","design","ux","career"
        ]
        tag_objs = []
        for name in tag_names:
            obj, _ = Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            tag_objs.append(obj)

        # author: prefer existing user or create demo user
        User = get_user_model()
        if User.objects.exists():
            author = User.objects.filter(is_staff=False).first() or User.objects.first()
        else:
            author = User.objects.create_user(username="demo_author", email="demo@example.com", password="demo12345")
            self.stdout.write("Created demo user 'demo_author' with password 'demo12345'")

        self.stdout.write(f"Creating {posts_to_create} posts...")
        for i in range(1, posts_to_create + 1):
            title = fake.sentence(nb_words=random.randint(5,10)).rstrip(".")
            slug = f"{slugify(title)}-{i}"
            body = "\n\n".join(fake.paragraphs(nb=random.randint(4,8)))
            created_at = timezone.now() - timedelta(days=random.randint(0,365), hours=random.randint(0,23))

            category = random.choice(category_objs)

            post = Post.objects.create(
                title=title,
                slug=slug[:300],
                body=body,
                author=author,
                created_at=created_at,
                category=category, 
            )

            sample_tags = random.sample(tag_objs, random.randint(2,6))
            post.tags.add(*sample_tags)

            if i % 10 == 0:
                self.stdout.write(f"  created {i} posts")

        self.stdout.write(self.style.SUCCESS(f"Done: created {posts_to_create} posts."))
        self.stdout.write("You can export them with: python manage.py dumpdata api --indent 2 > fixtures/posts_100.json")
