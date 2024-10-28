from django.contrib import admin
from .models import Order
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum

class DateRangeFilter(admin.SimpleListFilter):
    title = 'Date Range'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('daily', 'Today'),
            ('weekly', 'This Week'),
            ('monthly', 'This Month'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        today = now().date()
        if value == 'daily':
            return queryset.filter(created_at__date=today)
        elif value == 'weekly':
            start_of_week = today - timedelta(days=today.weekday())
            return queryset.filter(created_at__date__gte=start_of_week)
        elif value == 'monthly':
            start_of_month = today.replace(day=1)
            return queryset.filter(created_at__date__gte=start_of_month)
        return queryset

class OrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'amount', 'ordered', 'created_at', 'daily_total', 'weekly_total', 'monthly_total')
    search_fields = ('user__email', 'name', 'email')
    list_filter = (DateRangeFilter,)
    class Media:
        js = ('assets/js/date_range_filter.js',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def daily_total(self, obj):
        today = now().date()
        total = Order.objects.filter(created_at__date=today).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return total

    def weekly_total(self, obj):
        start_of_week = now().date() - timedelta(days=now().date().weekday())
        total = Order.objects.filter(created_at__date__gte=start_of_week).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return total

    def monthly_total(self, obj):
        start_of_month = now().date().replace(day=1)
        total = Order.objects.filter(created_at__date__gte=start_of_month).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return total
    def get_list_display(self, request):
        if request.user.is_superuser:
            date_range = request.GET.get('date_range', 'all')
        
            if date_range == 'daily':
                return ('email', 'name', 'amount', 'ordered', 'created_at', 'daily_total')
            elif date_range == 'weekly':
                return ('email', 'name', 'amount', 'ordered', 'created_at', 'weekly_total')
            elif date_range == 'monthly':
                return ('email', 'name', 'amount', 'ordered', 'created_at', 'monthly_total')
        
            return ('email', 'name', 'amount', 'ordered', 'created_at', 'daily_total', 'weekly_total', 'monthly_total')
    
        return ('name', 'amount', 'ordered')


admin.site.register(Order, OrderAdmin)
