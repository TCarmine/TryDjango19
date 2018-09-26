from django.contrib import admin

#relative import

from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    #check docs
    list_display = ["title","updated","timestamp"]
    list_display_links = ["updated"]
    list_filter=["updated","title"]
    #only those in list_display
    list_editable = ["title"]
    #list_display_filter = ["updated","timestamp"]

    search_fields = ["title","content"]
    class Meta:
        model = Post

admin.site.register(Post,PostModelAdmin)
