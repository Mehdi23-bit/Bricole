#!/bin/bash

echo "Starting Celery Beat and Worker in separate tabs..."

# Simple gnome-terminal approach
gnome-terminal --tab --title="Celery Beat" -- bash -c "
echo 'Starting Celery Beat...';
celery -A Bricole beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler;
exec bash
" &

gnome-terminal --tab --title="Celery Worker" -- bash -c "
echo 'Starting Celery Worker...';
celery -A Bricole worker --loglevel=info;
exec bash
" &

echo "Both services started in separate terminal tabs!"