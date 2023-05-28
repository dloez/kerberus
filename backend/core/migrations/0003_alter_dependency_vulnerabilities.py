# Generated by Django 4.1.7 on 2023-05-28 13:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_dependency_total_vulnerabilities_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dependency",
            name="vulnerabilities",
            field=models.ManyToManyField(
                related_name="dependencies", through="core.VulnerabilityDependency", to="core.vulnerability"
            ),
        ),
    ]
