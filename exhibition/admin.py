from django.contrib import admin
from .models import Category, Material, Exhibition, Piece, ExhibitionLike, ExhibitionClick, ExhibitionShare, PieceClick, \
    PieceLike, PieceShare, InitialLike, Comment, GuestBook, ExhibitionMode, ExternalExhibition


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ModeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(ExhibitionMode, ModeAdmin)
admin.site.register(Exhibition)
admin.site.register(Piece)
admin.site.register(ExhibitionLike)
admin.site.register(PieceLike)
admin.site.register(ExhibitionClick)
admin.site.register(PieceClick)
# admin.site.register(ExhibitionShare)
# admin.site.register(PieceShare)
admin.site.register(InitialLike)
admin.site.register(Comment)
admin.site.register(GuestBook)
admin.site.register(ExternalExhibition)
