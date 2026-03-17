import { TestBed } from '@angular/core/testing';

import { RiskProfileService } from '../../core/services/risk-profile.service';

describe('RiskProfileService', () => {
  let service: RiskProfileService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RiskProfileService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
