import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TransactionMonitoringComponent } from './transaction-monitoring.component';

describe('TransactionMonitoringComponent', () => {
  let component: TransactionMonitoringComponent;
  let fixture: ComponentFixture<TransactionMonitoringComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TransactionMonitoringComponent]
    });
    fixture = TestBed.createComponent(TransactionMonitoringComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
