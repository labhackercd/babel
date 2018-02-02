# Generated by Django 2.0.2 on 2018-02-02 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('author_type', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(blank=True, max_length=200, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('cep', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('command', models.TextField()),
            ],
            options={
                'verbose_name': 'channel',
                'verbose_name_plural': 'channels',
            },
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('periodicity', models.IntegerField(default=0, help_text='Run script every X seconds')),
                ('manifestation_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collects', to='core.Channel')),
            ],
            options={
                'verbose_name': 'collect',
                'verbose_name_plural': 'collects',
            },
        ),
        migrations.CreateModel(
            name='CollectAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('collect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attrs', to='core.Collect')),
            ],
            options={
                'verbose_name': 'collect attribute',
                'verbose_name_plural': 'collect attributes',
            },
        ),
        migrations.CreateModel(
            name='CollectDomainAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=150)),
                ('is_mandatory', models.BooleanField(default=False)),
                ('manifestation_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collect_domain_attrs', to='core.Channel')),
            ],
            options={
                'verbose_name': 'Collect Domain Attribute',
                'verbose_name_plural': 'Collect Domain Attributes',
            },
        ),
        migrations.CreateModel(
            name='CollectManifestation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('collect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Collect')),
            ],
        ),
        migrations.CreateModel(
            name='Manifestation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_channel', models.CharField(max_length=200)),
                ('version', models.IntegerField(default=1)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('collect', models.ManyToManyField(through='core.CollectManifestation', to='core.Collect')),
            ],
            options={
                'verbose_name': 'manifestation',
                'verbose_name_plural': 'manifestations',
            },
        ),
        migrations.CreateModel(
            name='ManifestationAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('manifestation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attrs', to='core.Manifestation')),
            ],
            options={
                'verbose_name': 'manifestation attribute',
                'verbose_name_plural': 'manifestation attributes',
            },
        ),
        migrations.CreateModel(
            name='ManifestationDomainAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=150)),
                ('is_mandatory', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Manifestation Domain Attribute',
                'verbose_name_plural': 'Manifestation Domain Attributes',
            },
        ),
        migrations.CreateModel(
            name='ManifestationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manifestation_types', to='core.Channel')),
            ],
            options={
                'verbose_name': 'Manifestation Type',
                'verbose_name_plural': 'Manifestation Types',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('is_reference', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='core.Author')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='core.Channel')),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='ProfileAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attrs', to='core.Profile')),
            ],
            options={
                'verbose_name': 'profile attribute',
                'verbose_name_plural': 'profile attributes',
            },
        ),
        migrations.CreateModel(
            name='ProfileDomainAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=150)),
                ('is_mandatory', models.BooleanField(default=False)),
                ('manifestation_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_domain_attrs', to='core.Channel')),
            ],
            options={
                'verbose_name': 'Domain Attribute',
                'verbose_name_plural': 'Domain Attributes',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='manifestationdomainattribute',
            name='manifestation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manifestation_domain_attrs', to='core.ManifestationType'),
        ),
        migrations.AddField(
            model_name='manifestation',
            name='manifestation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manifestations', to='core.ManifestationType'),
        ),
        migrations.AddField(
            model_name='manifestation',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manifestations', to='core.Profile'),
        ),
        migrations.AddField(
            model_name='collectmanifestation',
            name='manifestation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Manifestation'),
        ),
        migrations.AlterUniqueTogether(
            name='manifestation',
            unique_together={('id_in_channel', 'version')},
        ),
    ]
