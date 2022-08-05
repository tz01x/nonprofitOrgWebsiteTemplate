# Generated by Django 3.2.6 on 2022-08-05 00:43

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20220805_0643'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title of Club Roles & Responsibilities')),
            ],
            options={
                'verbose_name': ' Club Roles & Responsibilities',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MemberHierarchyLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.SmallIntegerField(help_text='smaller the number is the higer the priority gets', verbose_name='Priority of Current Roles')),
                ('name', models.CharField(max_length=500, verbose_name='Level name')),
            ],
            options={
                'verbose_name': ' Member HierarchyLevel',
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RegMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Member Full name')),
                ('university_id', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=11, verbose_name='phoneNumber')),
                ('bloodGroup', models.CharField(choices=[('A (+ve)', 'A (+ve)'), ('A (-ve)', 'A (-ve)'), ('AB (+ve)', 'AB (+ve)'), ('AB (-ve)', 'AB (-ve)'), ('B (+ve)', 'B (+ve)'), ('B (-ve)', 'B (-ve)'), ('O (+ve)', 'O (+ve)'), ('O (-ve)', 'O (-ve)')], default='unknown', max_length=10)),
                ('email', models.EmailField(max_length=150)),
                ('facebook_profile_url', models.URLField(blank=True, max_length=150, null=True)),
                ('linkin_url', models.URLField(blank=True, max_length=150, null=True)),
                ('portfolio_url', models.URLField(blank=True, max_length=500, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=core.models.ImageUploderPath.uploadTo, verbose_name='Member picture (1:1 ratio is recommended)')),
                ('created', models.DateField(auto_now=True)),
                ('joined', models.BooleanField(default=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='reg_member', to='members.department')),
                ('skill', models.ManyToManyField(related_name='reg_members', to='members.Skill')),
            ],
            options={
                'verbose_name': 'Newly Register Members',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='members.memberhierarchylevel', verbose_name='HierarchyLevel')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='members.clubroles')),
                ('semesters', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.semester', verbose_name='Club year')),
            ],
            options={
                'verbose_name': ' Position',
                'ordering': ['semesters', 'priority'],
            },
        ),
        migrations.CreateModel(
            name='MemberViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, help_text="Don't need to fill this, because this field will be automatically generate", max_length=255, null=True, unique=True)),
                ('title', models.CharField(max_length=250, verbose_name='Page title')),
                ('roles', models.ManyToManyField(to='members.ClubRoles', verbose_name='Which which member in selected roles will be will be showen in the the page.')),
            ],
            options={
                'verbose_name': 'Members view',
            },
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Member Full name')),
                ('is_alumni', models.BooleanField(default=False)),
                ('discription', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('university_id', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=500)),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='phoneNumber')),
                ('bloodGroup', models.CharField(choices=[('A (+ve)', 'A (+ve)'), ('A (-ve)', 'A (-ve)'), ('AB (+ve)', 'AB (+ve)'), ('AB (-ve)', 'AB (-ve)'), ('B (+ve)', 'B (+ve)'), ('B (-ve)', 'B (-ve)'), ('O (+ve)', 'O (+ve)'), ('O (-ve)', 'O (-ve)')], default='unknown', max_length=10)),
                ('facebook_profile_url', models.URLField(blank=True, max_length=500, null=True)),
                ('linkin_url', models.URLField(blank=True, max_length=500, null=True)),
                ('portfolio_url', models.URLField(blank=True, max_length=500, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=core.models.ImageUploderPath.uploadTo, verbose_name='Member picture  (1:1 ratio is recommended)')),
                ('created', models.DateField(auto_now_add=True, db_index=True, null=True)),
                ('join_at', models.DateField(verbose_name='Joined Date')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.department')),
                ('positions', models.ManyToManyField(to='members.Position')),
                ('priority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.memberhierarchylevel', verbose_name='HierarchyLevel')),
                ('semesters', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_members', to='core.semester', verbose_name='Club Year')),
                ('skill', models.ManyToManyField(related_name='members', to='members.Skill')),
            ],
            options={
                'verbose_name': 'Member',
                'ordering': ['semesters', 'priority'],
            },
        ),
    ]
