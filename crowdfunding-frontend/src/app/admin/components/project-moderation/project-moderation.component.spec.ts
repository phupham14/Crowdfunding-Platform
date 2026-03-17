import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectModerationComponent } from './project-moderation.component';

describe('ProjectModerationComponent', () => {
  let component: ProjectModerationComponent;
  let fixture: ComponentFixture<ProjectModerationComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ProjectModerationComponent]
    });
    fixture = TestBed.createComponent(ProjectModerationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
