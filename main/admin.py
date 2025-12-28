from django.contrib import admin

from main.models import (
    Author,
    Book,
    BookCopy,
    Category,
    Member,
    Borrowing,
)

# Global Admin Customization

admin.site.site_header = "Library Management System"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Administration Panel"

# Author Admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'about')
    search_fields = ('name',)
    ordering = ('name',)

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BookCopyInline(admin.TabularInline):
    model = BookCopy
    fields = ('unique_id', 'is_available')
    # readonly_fields = ('unique_id',)

# Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'is_published', 'isbn', 'get_available_copies')
    search_fields = ('title', 'author__name')
    list_filter = ('is_published', 'category',)
    ordering = ('title',)
    list_editable = ('is_published',)

    # form view
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'cover_image', 'digital_book', 'get_available_copies')
        }),
        ('Relations', {
            'fields': ('category', 'author'),
        }
        ),
        ('Publication Details', {
            'fields': ('publication_date', 'isbn', 'is_published'),
            'classes': ('collapse',)
        }
        )
        )

    autocomplete_fields = ('author',)
    filter_horizontal = ('category',)

    readonly_fields = ()
    inlines = [BookCopyInline]

    actions = ['publish_books', 'unpublish_books']

    


    def publish_books(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, "Selected books have been published.")
    publish_books.short_description = "Publish selected books"

    def unpublish_books(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, "Selected books have been unpublished.")
    unpublish_books.short_description = "Unpublish selected books"

    # custom methods
    def get_available_copies(self, obj):
        return obj.bookcopy_set.filter(is_available=True).count()

    get_available_copies.short_description = 'Available Copies'

    readonly_fields = ('get_available_copies',)

    # permissions
    def has_change_permission(self, request, obj=None):
        if obj and obj.is_published:
            return False
        return super().has_change_permission(request, obj)

    # save hook
    def save_model(self, request, obj, form, change):
        if not change:
            # New book, assign default permissions
            assign_perm('can_publish_book', request.user, obj)
        super().save_model(request, obj, form, change)


admin.site.register(Member)
admin.site.register(Borrowing)
admin.site.register(BookCopy)
