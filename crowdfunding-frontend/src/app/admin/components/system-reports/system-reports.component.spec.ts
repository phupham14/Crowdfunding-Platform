import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SystemReportsComponent } from './system-reports.component';

describe('SystemReportsComponent', () => {
  let component: SystemReportsComponent;
  let fixture: ComponentFixture<SystemReportsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SystemReportsComponent]
    });
    fixture = TestBed.createComponent(SystemReportsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
