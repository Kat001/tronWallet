from django.contrib import admin
from .models import Instructor, Course, Student, CourseModule, CourseTestimonial, CourseFAQ, ModuleVideo


admin.register(Instructor)
admin.register(Course)
admin.register(Student)
admin.register(CourseModule)
admin.register(CourseTestimonial)
admin.register(CourseFAQ)
admin.register(ModuleVideo)
