import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pygam

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score

from sklearn.cluster import KMeans

from sklearn.decomposition import PCA

class Modeler:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def testGAM(self, x, y):
        test_preds = self.model.predict(x)
        print(mse(y, test_preds))
        print(r2_score(y, test_preds))

    def split_data(self, test_size = 0.3):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size = test_size)

    def plotModel(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 4))
        fig.suptitle("Predictions vs. True Values", fontsize = 14, y = 1)
        plt.subplots_adjust(top = 0.93, wspace = 0)
        ax1.scatter(self.y_test, self.test_preds, s = 2, alpha = 0.5)
        ax1.plot(list(range(0, int(self.y_test.max()) + 10)), color = 'black', linestyle = '--')
        ax1.set_title("Test Set")
        ax1.set_xlabel("True Values")
        ax1.set_ylabel("Predictions")
        ax2.scatter(self.y_train, self.train_preds, s = 2, alpha = 0.5)
        ax2.plot(list(range(0, int(self.y_train.max()) + 10)), color = 'black', linestyle = '--')
        ax2.set_title("Train Set")
        ax2.set_xlabel("True Values")
        ax2.set_ylabel("")

        plt.show()

    def plotModel2(self):
        pca = PCA(n_components = 2)
        pca_result = pca.fit_transform(self.x_test)
        sns.scatterplot(x = pca_result[:,0], y = self.y_test, alpha = 0.5)
        sns.scatterplot(x = pca_result[:,0], y = self.test_preds, alpha = 0.5, color = "orange")
        plt.title('PCA Scatterplot')
        plt.xlabel("Principal Component 1")
        plt.ylabel("Price")
        plt.show()
        

    def gammer(self, n_splines = 21):
        self.model = pygam.GAM(n_splines = n_splines).fit(self.x_train,self.y_train)
        self.train_preds = self.model.predict(self.x_train)
        self.test_preds = self.model.predict(self.x_test)

        train_mse = mse(self.y_train, self.train_preds)
        test_mse = mse(self.y_test, self.test_preds)
        print(train_mse, test_mse)
        print("Train R2", r2_score(self.y_train, self.train_preds))
        print("Test R2", r2_score(self.y_test, self.test_preds))

    def gammerMulti(self):
        train_preds = []
        test_preds = []
        for i in range(5,50):
            print("Iter ",i)
            model = pygam.GAM(n_splines = i).fit(self.x_train,self.y_train)
            train_preds.append(mse(self.y_train,model.predict(self.x_train)))
            test_preds.append(mse(self.y_test,model.predict(self.x_test)))
        print(train_preds)
        print(test_preds)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 4))
        fig.suptitle("Train Error vs. Test Error", fontsize = 14, y = 1)
        plt.subplots_adjust(top = 0.93, wspace = 0)
        ax1.plot(range(5,50), test_preds, linestyle='-', marker='o')
        ax1.set_title("Test Set")
        ax1.set_xlabel("N_Splines")
        ax1.set_ylabel("MSE")
        ax2.plot(range(5,50), train_preds, linestyle='-', marker='o')
        ax2.set_title("Train Set")
        ax2.set_xlabel("N_Splines")
        ax2.set_ylabel("")

        plt.show()

    def linreg(self, cv = 10):
        self.model = LinearRegression(normalize = True)
        self.model.fit(self.x_train, self.y_train)
        self.train_preds = self.model.predict(self.x_train)
        self.test_preds = self.model.predict(self.x_test)

        train_mse = mse(self.y_train, self.train_preds)
        test_mse = mse(self.y_test, self.test_preds)
        print(train_mse, test_mse)
        print("Train R2", r2_score(self.y_train, self.train_preds))
        print("Test R2", r2_score(self.y_test, self.test_preds))

    def polyreg(self, degree = 2):
        poly = PolynomialFeatures(degree)
        x_train = poly.fit_transform(self.x_train)
        x_test = poly.fit_transform(self.x_test)
        self.model = LassoCV(cv = 20, normalize = True)
        self.model.fit(x_train, self.y_train)
        self.train_preds = self.model.predict(x_train)
        self.test_preds = self.model.predict(x_test)

        train_mse = mse(self.y_train, self.train_preds)
        test_mse = mse(self.y_test, self.test_preds)
        print(train_mse, test_mse)
        print("Train R2", r2_score(self.y_train, self.train_preds))
        print("Test R2", r2_score(self.y_test, self.test_preds))

    def lassoer(self, cv = 20):
        self.model = LassoCV(cv = cv, normalize = True)
        self.model.fit(self.x_train, self.y_train)
        self.train_preds = self.model.predict(self.x_train)
        self.test_preds = self.model.predict(self.x_test)

        train_mse = mse(self.y_train, self.train_preds)
        test_mse = mse(self.y_test, self.test_preds)
        print(train_mse, test_mse)
        print("Train R2", r2_score(self.y_train, self.train_preds))
        print("Test R2", r2_score(self.y_test, self.test_preds))


    def ridger(self, cv = 20):
        self.model = RidgeCV(cv = cv, normalize = True)
        self.model.fit(self.x_train, self.y_train)
        self.train_preds = self.model.predict(self.x_train)
        self.test_preds = self.model.predict(self.x_test)

        train_mse = mse(self.y_train, self.train_preds)
        test_mse = mse(self.y_test, self.test_preds)
        print(train_mse, test_mse)
        print("Train R2", r2_score(self.y_train, self.train_preds))
        print("Train R2", r2_score(self.y_test, self.test_preds))

class Listings:
    def __init__(self, filename = 'chicago_listings.csv', groupAmenities = True, DATT = True):
        # pd.set_option('display.max_columns', 500)
        self.readListings(filename)
        self.groupAmenities = groupAmenities
        if DATT:
            self.dropCols()
            self.cleaner()

    def corrHeatMap(self):
        corr = self.df.select_dtypes(include = 'number').drop('id', axis = 1).corr()
        mask = np.zeros_like(corr, dtype = np.bool)
        mask[np.tril_indices_from(mask)] = True
        f, ax = plt.subplots(figsize = (11, 9))
        cmap = sns.diverging_palette(220, 10, as_cmap = True)
        sns.heatmap(corr, mask = mask, cmap = cmap, vmax = 0.3, center = 0, square = True, linewidths = 0.5, cbar_kws = {'shrink': 0.5})
        plt.show()
    
    def readListings(self, filename):

        # suppress low_memory warning--file isn't large enough for
        # any significant processing impact.
        self.df = pd.read_csv(filename, low_memory = False)
        self.df.set_index('id')
        self.columns = self.df.columns.values.tolist()

    def longLat(self, k = 10, showplot = False):
        '''Use KMeans to categorize lat/long into our own version of neighborhoods.
        Set k = -1 to graph error for k=1:20. Otherwise, set K and returns kmeans.
        8 was found to be a good number.'''
        if k <= 0:
            print("Fitting 35 ks")
            cluster_sum_squares = []
            for i in range(1, 35):
                print("iteration", i)
                kmeans = KMeans(n_clusters = i, init = 'k-means++')
                kmeans.fit(self.df[['latitude', 'longitude']].copy())
                cluster_sum_squares.append(kmeans.inertia_)
            plt.plot(range(1,35), cluster_sum_squares)
            plt.xlabel("# Clusters")
            plt.ylabel("Cluster Sum of Squares")
            plt.title("K-Means Neighborhood Clustering")
            plt.show()
            return kmeans
            
        kmeans = KMeans(n_clusters = k, init = 'k-means++')
        labels = kmeans.fit_predict(self.df[['latitude', 'longitude']].copy())
        if showplot:
            sns.scatterplot(self.df.longitude, self.df.latitude, alpha=0.3)
            sns.scatterplot(kmeans.cluster_centers_[:,1], kmeans.cluster_centers_[:,0])
            plt.show()
        self.df['kmeans_neighborhoods'] = labels
        self.df.kmeans_neighborhoods = self.df.kmeans_neighborhoods.astype('category')
        self.df.drop(['latitude','longitude'], axis = 1)
        return kmeans

    def nullVals(self, column):
        return self.df[column].isna().sum()

    def fillNulls(self, column, newNull):
        self.df[column] = self.df[column].fillna(newNull)

    def dollarToFloat(self, column):
        if type(self.df[column][0]) != str:
            print("Data is not a string")
        else:
            self.df[column] = self.df[column].str.replace('$', '').str.replace(',','').astype(float)

    def dropCols(self, toDrop = [
            'summary', 'space', 'description', 'neighborhood_overview',
            'notes', 'transit', 'access', 'interaction',
            'house_rules', 'thumbnail_url', 'host_about', 'license',
            'listing_url', 'scrape_id', 'last_scraped', 'name',
            'medium_url', 'picture_url', 'xl_picture_url', 'host_id', 'host_since',
            'host_location', 'host_acceptance_rate', 'host_neighbourhood',
            'host_listings_count', 'host_total_listings_count',
            'host_url', 'host_name', 'host_thumbnail_url', 'host_picture_url',
            'neighbourhood', 'neighbourhood_cleansed', 'neighbourhood_group_cleansed',
            'city', 'state', 'street', 'zipcode', 'market', 'smart_location', 'country_code',
            'country', 'is_location_exact',
            'weekly_price', 'monthly_price', 'square_feet',
            'minimum_nights', 'minimum_minimum_nights', 'maximum_minimum_nights',
            'maximum_nights', 'minimum_maximum_nights', 'maximum_maximum_nights',
            'calendar_updated', 'calendar_last_scraped',
            'number_of_reviews_ltm', 'first_review', 'last_review',
            'jurisdiction_names', 'experiences_offered',
            'host_verifications']):
        self.df = self.df.drop(toDrop, axis = 1)
        self.columns = self.df.columns.values.tolist()

    def cleaner(self):

        #convert property types to an index
        self.property_types = self.df.property_type.unique().tolist()
        self.property_types_index = {}
        for i in range(len(self.property_types)):
            self.property_types_index[self.property_types[i]] = i
        self.df.property_type = self.df.property_type.apply(lambda x: self.property_types_index[x]).astype('category')

        #convert room types to an index
        self.room_types = self.df.room_type.unique().tolist()
        self.room_types_index = {}
        for i in range(len(self.room_types)):
            self.room_types_index[self.room_types[i]] = i
        self.df.room_type = self.df.room_type.apply(lambda x: self.room_types_index[x]).astype('category')

        #convert bed types to an index
        self.bed_types = self.df.bed_type.unique().tolist()
        self.bed_types_index = {}
        for i in range(len(self.bed_types)):
            self.bed_types_index[self.bed_types[i]] = i
        self.df.bed_type = self.df.bed_type.apply(lambda x: self.bed_types_index[x]).astype('category')

        #convert cancellation policy to an index
        self.cancellation_policies = self.df.cancellation_policy.unique().tolist()
        self.cancellation_policies_index = {}
        for i in range(len(self.cancellation_policies)):
            self.cancellation_policies_index[self.cancellation_policies[i]] = i
        self.df.cancellation_policy = self.df.cancellation_policy.apply(lambda x: self.cancellation_policies_index[x]).astype('category')

        #convert response time to an index
        self.response_times = self.df.host_response_time.unique().tolist()
        self.response_times_index = {}
        for i in range(len(self.response_times)):
            self.response_times_index[self.response_times[i]] = i
        self.df.host_response_time = self.df.host_response_time.apply(lambda x: self.response_times_index[x]).astype('category')

        #convert binary values to bool
        self.df.host_is_superhost = self.df.host_is_superhost.apply(lambda x: x == 't')
        self.df.host_has_profile_pic = self.df.host_has_profile_pic.apply(lambda x: x == 't')
        self.df.host_identity_verified = self.df.host_identity_verified.apply(lambda x: x == 't')
        self.df.has_availability = self.df.has_availability.apply(lambda x: x == 't')
        self.df.availability_30 = self.df.availability_30.apply(lambda x: x == 't')
        self.df.availability_60 = self.df.availability_60.apply(lambda x: x == 't')
        self.df.availability_90 = self.df.availability_90.apply(lambda x: x == 't')
        self.df.availability_365 = self.df.availability_365.apply(lambda x: x == 't')
        self.df.requires_license = self.df.requires_license.apply(lambda x: x == 't')
        self.df.instant_bookable = self.df.instant_bookable.apply(lambda x: x == 't')
        self.df.is_business_travel_ready = self.df.is_business_travel_ready.apply(lambda x: x == 't')
        self.df.require_guest_profile_picture = self.df.require_guest_profile_picture.apply(lambda x: x == 't')
        self.df.require_guest_phone_verification = self.df.require_guest_phone_verification.apply(lambda x: x == 't')

        #convert dollars to floats
        self.dollarToFloat('price')
        self.dollarToFloat('extra_people')
        self.fillNulls('cleaning_fee', '0') #Assuming missing cleaning fees indicates 0 charge.
        self.dollarToFloat('cleaning_fee')
        self.fillNulls('security_deposit', '0')
        self.dollarToFloat('security_deposit')

        #convert host response rate to float
        self.df.host_response_rate = self.df.host_response_rate.str.replace('%', '').astype(float) / 100
        self.fillNulls('host_response_rate', self.df.host_response_rate.mean())
        
        #clean up other null vals
        self.fillNulls('bathrooms', 1.0)
        self.fillNulls('bedrooms', 1.0)
        self.fillNulls('beds', 1.0)

        self.fillNulls('review_scores_rating', self.df.review_scores_rating.mean())
        self.fillNulls('review_scores_accuracy', self.df.review_scores_accuracy.mean())
        self.fillNulls('review_scores_cleanliness', self.df.review_scores_cleanliness.mean())
        self.fillNulls('review_scores_checkin', self.df.review_scores_checkin.mean())
        self.fillNulls('review_scores_communication', self.df.review_scores_communication.mean())
        self.fillNulls('review_scores_location', self.df.review_scores_location.mean())
        self.fillNulls('review_scores_value', self.df.review_scores_value.mean())
        self.fillNulls('reviews_per_month', 0)

        #set kmeans neighborhoods using estimated best k=20 option
        self.longLat(k = 20)

        if self.groupAmenities:
            self.df.amenities = self.df.amenities.apply(lambda x: len(x.split(',')))
        else:
            amenities = set()
            for listing in self.df.amenities:
                replacements = ['{', '}', '"']
                for r in replacements:
                    listing = listing.replace(r, '').lower()
                spacers = ['/', ':', ';', '-', '(', ')', '&']
                for s in spacers:
                    listing = listing.replace(s, '_')
                l = listing.split(',')
                for am in l:
                    amenities.add(am)
            for amenity in amenities:
                if amenity != "" and 'missing' not in amenity:
                    self.df[amenity] = self.df.amenities.apply(lambda x: amenity in x)

            self.df = self.df.drop('amenities', axis = 1)
            self.columns = self.df.columns.values.tolist()

        #Drop outliers past the 95% quantile
        q = self.df.price.quantile(0.95)
        self.df = self.df[self.df.price <= q]

        self.df = self.df.drop(['id', 'longitude', 'latitude'], axis = 1)
        

        self.y = self.df.price
        self.x = self.df.drop(['price'], axis = 1)
        self.y.to_csv(r'y.csv', index = None, header = True)
        self.x.to_csv(r'x.csv', index = None, header = True)
