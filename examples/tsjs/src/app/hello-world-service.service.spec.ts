import { TestBed, inject } from '@angular/core/testing';
import { HelloWorldServiceService } from './hello-world-service.service';

describe('Hello-World-Service-Service', () => {
beforeEach(() => {
    TestBed.configureTestingModule({
    providers: [HelloWorldServiceService]
    });
});
// Test that the service is present.
it('should be created', () => {
    const service: HelloWorldServiceService = TestBed.get(HelloWorldServiceService);
    expect(service).toBeTruthy();
  });

// Test that the add function is present
it ('test the add function',
inject([HelloWorldServiceService], (service: HelloWorldServiceService ) => {
    expect(service.add).toBeTruthy();
}));

// Perform addition
it('should perform addition correctly',
inject([HelloWorldServiceService], (service: HelloWorldServiceService) => {
    expect(service.add(100, 200)).toEqual(300);
}));

// Perform concatination
it('should perform concatination correctly',
inject([HelloWorldServiceService], (service: HelloWorldServiceService) => {
    expect(service.concat('hello', 'kitty')).toEqual('hellokitty');
}));


});
