import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RiskProfileComponent } from './risk-profile.component';

describe('RiskProfileComponent', () => {
  let component: RiskProfileComponent;
  let fixture: ComponentFixture<RiskProfileComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RiskProfileComponent]
    });
    fixture = TestBed.createComponent(RiskProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
