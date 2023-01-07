


describe('helloworld', () => {


    let expected = '';
    let notexpected = '';
    let regexMatch = null;

    beforeEach(() => {
        expected = 'helloKitty';
        notexpected = 'helloPuppy';
        regexMatch = new RegExp(/^hello/);

    });

    afterEach(() => {
        expected = '';
        notexpected = '';
        regexMatch = null;
    });


    it('check a static string to be',
        () => expect('helloKitty').toBe(expected));

    it('check a static string not to be',
        () => expect('helloKitty').not.toBe(notexpected));

    it('check a static string regex match',
        () => expect('helloKitty').toMatch(regexMatch));


});
