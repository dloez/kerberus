# Generated by Django 4.1.7 on 2023-05-14 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dependency",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("version", models.CharField(max_length=20)),
                ("ecosystem", models.CharField(choices=[("maven", "maven"), ("npm", "npm")], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Vulnerability",
            fields=[
                ("osv_id", models.CharField(max_length=100, primary_key=True, serialize=False)),
                ("cve_id", models.CharField(max_length=100, null=True)),
                ("severity", models.CharField(max_length=100, null=True)),
                ("severity_base_score", models.FloatField(null=True)),
                (
                    "severity_base_score_string",
                    models.CharField(
                        choices=[
                            ("NONE", "NONE"),
                            ("LOW", "LOW"),
                            ("MEDIUM", "MEDIUM"),
                            ("HIGH", "HIGH"),
                            ("CRITICAL", "CRITICAL"),
                        ],
                        max_length=8,
                        null=True,
                    ),
                ),
                ("severity_temporal_score", models.FloatField(null=True)),
                (
                    "severity_temporal_score_string",
                    models.CharField(
                        choices=[
                            ("NONE", "NONE"),
                            ("LOW", "LOW"),
                            ("MEDIUM", "MEDIUM"),
                            ("HIGH", "HIGH"),
                            ("CRITICAL", "CRITICAL"),
                        ],
                        max_length=8,
                        null=True,
                    ),
                ),
                ("severity_environmental_score", models.FloatField(null=True)),
                (
                    "severity_environmental_score_string",
                    models.CharField(
                        choices=[
                            ("NONE", "NONE"),
                            ("LOW", "LOW"),
                            ("MEDIUM", "MEDIUM"),
                            ("HIGH", "HIGH"),
                            ("CRITICAL", "CRITICAL"),
                        ],
                        max_length=8,
                        null=True,
                    ),
                ),
                ("severity_overall_score", models.FloatField(null=True)),
                (
                    "severity_overall_score_string",
                    models.CharField(
                        choices=[
                            ("NONE", "NONE"),
                            ("LOW", "LOW"),
                            ("MEDIUM", "MEDIUM"),
                            ("HIGH", "HIGH"),
                            ("CRITICAL", "CRITICAL"),
                        ],
                        max_length=8,
                        null=True,
                    ),
                ),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="VulnerabilityDependency",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fixed_versions", models.CharField(max_length=255)),
                ("dependency", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.dependency")),
                (
                    "vulnerability",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.vulnerability"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("dependencies", models.ManyToManyField(related_name="projects", to="core.dependency")),
            ],
        ),
        migrations.CreateModel(
            name="Ingest",
            fields=[
                ("hash_id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("ecosystem", models.CharField(choices=[("maven", "maven"), ("npm", "npm")], max_length=10)),
                ("dependencies", models.ManyToManyField(related_name="ingests", to="core.dependency")),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.project")),
            ],
        ),
        migrations.AddField(
            model_name="dependency",
            name="ingest",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.ingest"),
        ),
        migrations.AddField(
            model_name="dependency",
            name="vulnerabilities",
            field=models.ManyToManyField(through="core.VulnerabilityDependency", to="core.vulnerability"),
        ),
    ]