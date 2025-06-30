import requests
from .models import Project, SyncLog
from django.conf import settings

def fetch_upwork_projects():
    # Shembull: përdor një endpoint fiktiv, zëvendëso me të vërtetin sipas nevojës
    url = getattr(settings, 'UPWORK_API_URL', 'https://api.upwork.com/example/projects')
    headers = {
        'Authorization': f'Bearer {getattr(settings, "UPWORK_API_TOKEN", "")}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        imported, skipped = 0, 0
        for item in data.get('projects', []):
            upwork_id = item.get('id')
            if not upwork_id:
                continue
            project, created = Project.objects.get_or_create(
                upwork_id=upwork_id,
                defaults={
                    'name': item.get('title', f'Upwork Project {upwork_id}'),
                    'description': item.get('description', '')
                }
            )
            if created:
                imported += 1
            else:
                skipped += 1
        SyncLog.objects.create(status='success', message=f'Imported: {imported}, Skipped: {skipped}')
        return {'imported': imported, 'skipped': skipped}
    except Exception as e:
        SyncLog.objects.create(status='failed', message=str(e))
        return {'error': str(e)} 