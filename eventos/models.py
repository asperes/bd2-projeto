from django.db import models
from utilizadores.models import User

# Create your models here.


class VActiveEvents(models.Model):                  #vista para eventos activos
    event_id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    is_public = models.BooleanField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    host_id = models.UUIDField()
    host_username = models.CharField(max_length=150)
    host_first_name = models.CharField(max_length=150)
    host_last_name = models.CharField(max_length=150)
    attendee_count = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'v_active_events'



class Checkins(models.Model):
    checkin_id = models.UUIDField(primary_key=True)
    event = models.ForeignKey('Events', models.DO_NOTHING)
    user = models.ForeignKey('utilizadores.User', models.DO_NOTHING)
    checked_in_at = models.DateTimeField(blank=True, null=True)
    checked_out_at = models.DateTimeField(blank=True, null=True)
    location_latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    location_longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checkins'
        db_table_comment = 'Tracks user attendance and check-ins at events'


class EventActivities(models.Model):
    activity_id = models.UUIDField(primary_key=True)
    event = models.ForeignKey('Events', models.DO_NOTHING)
    user = models.ForeignKey('utilizadores.User', models.DO_NOTHING)
    activity_type = models.CharField(max_length=50)
    activity_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_activities'
        db_table_comment = 'Activity feed for events tracking all user actions'


class EventAnalytics(models.Model):
    analytics_id = models.UUIDField(primary_key=True)
    event = models.ForeignKey('Events', models.DO_NOTHING)
    total_attendees = models.IntegerField(blank=True, null=True)
    total_messages = models.IntegerField(blank=True, null=True)
    total_media = models.IntegerField(blank=True, null=True)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    engagement_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    peak_concurrent_users = models.IntegerField(blank=True, null=True)
    calculated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_analytics'
        db_table_comment = 'Daily analytics snapshots for events'


class EventCohosts(models.Model):
    cohost_id = models.UUIDField(primary_key=True)
    event = models.ForeignKey('Events', models.DO_NOTHING)
    user = models.ForeignKey('utilizadores.User', models.DO_NOTHING)
    permissions = models.JSONField(blank=True, null=True)
    added_by = models.ForeignKey('utilizadores.User', models.DO_NOTHING, db_column='added_by', related_name='eventcohosts_added_by_set')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_cohosts'
        unique_together = (('event', 'user'),)
        db_table_comment = 'Manages co-hosts with specific permissions for events'


class EventInvitations(models.Model):
    invitation_id = models.UUIDField(primary_key=True)
    event = models.ForeignKey('Events', models.DO_NOTHING)
    inviter = models.ForeignKey('utilizadores.User', models.DO_NOTHING)
    invitee = models.ForeignKey('utilizadores.User', models.DO_NOTHING, related_name='eventinvitations_invitee_set')
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    role = models.TextField(blank=True, null=True)  # This field type is a guess.
    invited_at = models.DateTimeField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    notification_sent = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_invitations'
        unique_together = (('event', 'invitee'),)
        db_table_comment = 'Tracks event invitations and attendee responses'


class EventSeries(models.Model):
    series_id = models.UUIDField(primary_key=True)
    master_event = models.OneToOneField('Events', models.DO_NOTHING)
    recurrence_pattern = models.CharField(max_length=50)
    series_end_date = models.DateField(blank=True, null=True)
    exceptions = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_series'
        db_table_comment = 'Manages recurring event series and their patterns'


class Events(models.Model):
    event_id = models.UUIDField(primary_key=True)
    host = models.ForeignKey('utilizadores.User', models.DO_NOTHING)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    location_address = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    max_attendees = models.IntegerField(blank=True, null=True)
    is_public = models.BooleanField(blank=True, null=True)
    is_recurring = models.BooleanField(blank=True, null=True)
    recurrence_rule = models.JSONField(blank=True, null=True, db_comment='JSON object following iCalendar RRULE format for recurring events')
    cover_image_url = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    EVENT_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=EVENT_STATUS_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    settings = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'
        db_table_comment = 'Main events table storing event details and settings'

