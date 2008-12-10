
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from tagging.models import Tag
from tagging.fields import TagField
from comment_utils.moderation import CommentModerator, moderator


class PostManager(models.Manager):
    def active(self):
        return self.filter(active=True)

class Post(models.Model):
    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(_("slug"), unique=True)
    body = models.TextField(_("body"))
    active = models.BooleanField(default=False)
    create_date = models.DateTimeField(_("created"), default=datetime.now)
    pub_date = models.DateTimeField(_("published"), default=datetime.now)
    tags = TagField()
    
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ("-pub_date",)
    
    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_detail", (), {
            "year": self.pub_date.strftime("%Y"),
            "month": self.pub_date.strftime("%b").lower(),
            "day": self.pub_date.strftime("%d"),
            "slug": self.slug,
        })

class PostModerator(CommentModerator):
    akismet = True
    email_notification = True

moderator.register(Post, PostModerator)
