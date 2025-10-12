from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# ---------- helpers ----------
def cover_upload_to(instance, filename):
    return f"covers/{instance.author_id or 'anon'}/{filename}"

def avatar_upload_to(instance, filename):
    return f"avatars/{instance.user_id}/{filename}"

# ---------- core: Post ----------
class Post(models.Model):
    author       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title        = models.CharField(max_length=180)
    slug         = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt      = models.CharField(max_length=220, blank=True)
    cover        = models.ImageField(upload_to=cover_upload_to, blank=True, null=True)
    content      = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # unique slug on first save
        if not self.slug:
            base = slugify(self.title)[:180]
            slug = base
            i = 2
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def likes_count(self):
        return self.likes.count()

# ---------- social: Comment ----------
class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content    = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

# ---------- social: Like ----------
class Like(models.Model):
    post   = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    when   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user} likes {self.post}"

# ---------- optional: User Profile (extend built-in User cleanly) ----------
class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar  = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)
    bio     = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
