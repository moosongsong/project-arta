from django.contrib import admin
from .models import Category, Material, Exhibition, Piece, ExhibitionLike, ExhibitionClick, ExhibitionShare, PieceClick, \
    PieceLike, PieceShare, InitialLike, Comment, GuestBook


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('smallName',)}


class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Exhibition)
admin.site.register(Piece)
admin.site.register(ExhibitionLike)
admin.site.register(PieceLike)
admin.site.register(ExhibitionClick)
admin.site.register(PieceClick)
admin.site.register(ExhibitionShare)
admin.site.register(PieceShare)
admin.site.register(InitialLike)
admin.site.register(Comment)
admin.site.register(GuestBook)
